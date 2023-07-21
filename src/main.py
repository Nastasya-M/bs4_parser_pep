import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, MAIN_PEP_URL,
                       NOT_FOUND_PYTHON_VERSION_ERROR,
                       PARSER_ARCHIVE_SAVE_MESSAGE, PARSER_FINISH_MESSAGE,
                       PARSER_PROGRAM_ERROR, PARSER_START_MESSAGE,
                       PARSING_ARGUMENTS_MESSAGE)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response_soup


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_response_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_response_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    soup = get_response_soup(session, MAIN_DOC_URL)

    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException(NOT_FOUND_PYTHON_VERSION_ERROR)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text = re.search(pattern, a_tag.text)
        if text is not None:
            version, status = text.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_response_soup(session, downloads_url)

    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(PARSER_ARCHIVE_SAVE_MESSAGE.format(archive_path=archive_path))


def pep(session):
    soup = get_response_soup(session, MAIN_PEP_URL)

    section_tags = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    table_tag = find_tag(section_tags, 'tbody')
    tr_tags = table_tag.find_all('tr')
    results = [('Статус', 'Количество')]
    status_counter = {}
    for tr_tag in tqdm(tr_tags):
        pep_abbr = find_tag(tr_tag, 'abbr')
        preview_status = pep_abbr.text[1:]
        href = find_tag(tr_tag, 'a')['href']
        pep_url = urljoin(MAIN_PEP_URL, href)
        soup = get_response_soup(session, pep_url)
        card_dl_tag = find_tag(
            soup, 'dl', attrs={'class': 'rfc2822 field-list simple'})
        td = card_dl_tag.find(string='Status')
        status_on_page = td.find_parent().find_next_sibling().text
        if status_on_page not in EXPECTED_STATUS[preview_status]:
            error_message = (f'Несовпадающие статусы:\n'
                             f'{pep_url}\n'
                             f'Статус в карточке: {status_on_page}\n'
                             f'Ожидаемые статусы:'
                             f'{EXPECTED_STATUS[preview_status]}')
            logging.info(error_message)
        status_counter[status_on_page] = status_counter.get(status_on_page,
                                                            0) + 1
    for key, value in status_counter.items():
        results.append((key, value))
    results.append(('Total', sum(status_counter.values())))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(PARSER_START_MESSAGE)

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(PARSING_ARGUMENTS_MESSAGE.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)
    except Exception:
        logging.exception(PARSER_PROGRAM_ERROR, stack_info=True)
    logging.info(PARSER_FINISH_MESSAGE)


if __name__ == '__main__':
    main()
