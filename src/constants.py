from pathlib import Path

BASE_DIR = Path(__file__).parent

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

PARSER_ARCHIVE_SAVE_MESSAGE = 'Архив был загружен и сохранён: {archive_path}.'
PARSING_ARGUMENTS_MESSAGE = 'Аргументы командной строки: {args}.'
PARSER_FINISH_MESSAGE = 'Парсер завершил работу.'
NOT_FOUND_PYTHON_VERSION_ERROR = 'Не нашлось версий Python.'
PARSER_START_MESSAGE = 'Парсер запущен!'


PARSER_PROGRAM_ERROR = 'Возникла ошибка при выполнении.'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
