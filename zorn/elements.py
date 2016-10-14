class PageError(Exception):
    def __init__(self, message):
        super().__init__(self, message)


class Page:
    def __init__(self, page_name, file_name, sub_pages=None):
        self.page_name = page_name
        self.file_name = file_name
        if sub_pages is None:
            sub_pages = []

        for sub_page in sub_pages:
            if type(sub_page) is not SubPage:
                raise PageError(
                    'All elements of submenu have to be of type '
                    'zorn.Elements.SubPage'
                )

        self.sub_pages = sub_pages


class SubPage(Page):
    """A helper class to avoid attempts of creation of sub-sub pages"""

    def __init__(self, page_name, file_name):
        super().__init__(page_name, file_name, [])


class Website:
    def __init__(self, settings):
        self.__dict__ = settings