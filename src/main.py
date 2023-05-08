import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS_DIR_NAME, EXPECTED_STATUS,
                       MAIN_DOC_URL, MAIN_PEP_URL)
from outputs import control_output
from utils import find_tag, get_soup

WRONG_PEP_STATUS = (
    'Несовпадающий статус: {status} '
    'Ожидаемые статусы: {statuses}'
)
PROGRAMM_ERROR = (
    'Сбой в работе программы: {error}'
)
LOG = ('Архив был загружен и сохранён: {archive_path}')


def pep(session):
    logs = []
    tr_tags = get_soup(session, MAIN_PEP_URL).select(
        '#numerical-index tbody tr'
    )
    results = [('Статус', 'Количество')]
    pattern = r'Status: (?P<status>\w+)'
    statuses = {}
    for pep in tqdm(tr_tags):
        status_tag = pep.find('td')
        pep_a_tag = pep.find('a')
        pep_link = urljoin(MAIN_PEP_URL, pep_a_tag['href'])
        try:
            dl_tag = find_tag(get_soup(session, pep_link), 'dl')
        except ConnectionError as error:
            logs.append(error)
            continue
        dl_text = dl_tag.text.replace('\n', ' ')
        text_match = re.search(pattern, dl_text)
        status = text_match.group('status')
        expected_statuses = EXPECTED_STATUS[status_tag.text[1:]]
        if status not in expected_statuses:
            logs.append(
                WRONG_PEP_STATUS.format(
                    status=status,
                    statuses=expected_statuses
                )
            )
        if status not in statuses.keys():
            statuses[status] = 0
        statuses[status] += 1
    statuses['Total'] = sum(statuses.values())
    for log in logs:
        logging.info(log)
    for status in statuses.keys():
        results.append((status, statuses[status]))
    return results


def whats_new(session):
    logs = []
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    sections_by_python = get_soup(session, whats_new_url).select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        try:
            soup = get_soup(session, version_link)
        except ConnectionError as error:
            logs.append(error)
            continue
        results.append((
            version_link,
            find_tag(soup, 'h1').text,
            find_tag(soup, 'dl').text.replace('\n', ' ')
        ))
    return results


def latest_versions(session):
    for ul in get_soup(session, MAIN_DOC_URL).select(
        'div.sphinxsidebarwrapper ul'
    ):
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise KeyError('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in tqdm(a_tags):
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    pdf_a4_link = get_soup(session, downloads_url).select_one(
        'table.docutils a[href$="-docs-pdf-a4.zip"]'
    )['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    DOWNLOADS_DIR = BASE_DIR / DOWNLOADS_DIR_NAME
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(LOG.format(archive_path=archive_path))


MODE_TO_FUNCTION = {
    'pep': pep,
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(
            PROGRAMM_ERROR.format(error=error),
            stack_info=True
        )
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
