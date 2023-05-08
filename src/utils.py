from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

RESPONSE_ERROR = 'Возникла ошибка при загрузке страницы {url}'
ERROR_MESSAGE = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoder='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoder
        return response
    except RequestException:
        raise ConnectionError(RESPONSE_ERROR.format(url=url))


def get_soup(session, url):
    return BeautifulSoup(get_response(session, url).text, features='lxml')


def find_tag(soup, tag, attrs=None):
    find_attrs = {} if attrs is None else attrs
    searched_tag = soup.find(tag, attrs=find_attrs)
    if searched_tag is None:
        raise ParserFindTagException(
            ERROR_MESSAGE.format(tag=tag, attrs=attrs)
        )
    return searched_tag
