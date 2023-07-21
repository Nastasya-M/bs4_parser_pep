# Проект парсинга pep
### Описание 
```
Парсер собирает иформацию о документации Python https://docs.python.org/3/ и PEP https://peps.python.org/
```

### Технологи проекта:
```
Python
BeautifulSoup4
Prettytable
requests-cache
tqdm
Logging
```

### Как запустить проект:
Клонировать репозиторий:
```
git clone https://github.com/Nastasya-M/bs4_parser_pep
```
Создать виртуальное окружение:
```
python -m venv venv
```
Активировать виртуальное окружение и установить зависимости:
```
source venv/Scripts/activate
pip install -r requirements.txt
```
Перейти в директорию src/, запустить main.py и ознакомиться с документацией парсера:
```
cd src/
python main.py -h
```
### Документация парсера:
```
usage: main.py [-h] [-c] [-o {pretty,file}]
               {whats-new,latest-versions,download}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

### Проверка парсера:

Запуск парсера информации из статей о нововведениях в Python:
```
python main.py whats-new
```
Запуск парсера статусов версий Python:
```
python main.py latest-versions
```
Запуск парсера, который скачивает архив документации Python:
```
python main.py download
```
Запуск парсера, который скачивает список статусов документов PEP и количество PEP в каждом статусе:
```
python main.py pep
```