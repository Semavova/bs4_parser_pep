# Проект парсинга pep

## Парсинг документов PEP

> Парсер собирает данные обо всех PEP документах, сравнивает статусы и записывает их в файл, либо терминал

## Технологии проекта

- Python — язык программирования.
- BeautifulSoup4 - библиотека для парсинга.
- Prettytable - библиотека для удобного отображения табличных данных.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Semavova/bs4_parser_pep.git
```

```
cd bs4_parser_pep
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

## Примеры команд

Создаст csv файл с таблицей из двух колонок: «Статус» и «Количество»:

```
python main.py pep -o file
```

Выводит таблицу prettytable из двух колонок: «Статус» и «Количество»:

```
python main.py pep -o pretty 
```