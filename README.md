# Проект парсинга pep

## Парсинг документов PEP

Парсер собирает данные обо всех PEP документах, сравнивает статусы и записывает их в файл, либо терминал

## Технологии проекта

- Python — язык программирования.
- BeautifulSoup4 - библиотека для парсинга.
- Prettytable - библиотека для удобного отображения табличных данных.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/Semavova/bs4_parser_pep.git
```

```bash
cd bs4_parser_pep
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

## Примеры команд

Создаст csv файл с таблицей из двух колонок: «Статус» и «Количество»:

```bash
python main.py pep -o file
```

Выводит таблицу prettytable из двух колонок: «Статус» и «Количество»:

```bash
python main.py pep -o pretty 
```

Выводит таблицу prettytable с тремя колонками: "Ссылка на документацию", "Версия", "Статус":

```bash
python main.py latest-versions -o pretty 
```

Выводит ссылки на нововведения в python:

```bash
python main.py whats-new
```

Автор: [Владимир Семочкин](https://github.com/Semavova)
