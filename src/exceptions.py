class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class EmptyTagException(Exception):
    """Вызывается, когда парсер итерирует пустой тег"""
    pass
