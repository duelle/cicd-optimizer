import requests

from Configuration import BASE_URL, HEADERS


class TravisRepository:
    __json: str

    def __init__(self, repo_slug):
        self.__json = requests.get(f'{BASE_URL}/repo/{repo_slug}', headers=HEADERS).json()

    @property
    def id(self):
        # noinspection PyTypeChecker
        return self.__json['id']

    @property
    def slug(self) -> str:
        # noinspection PyTypeChecker
        return self.__json['slug']

    @property
    def name(self) -> str:
        # noinspection PyTypeChecker
        return self.__json['name']

    @property
    def default_branch_name(self) -> str:
        # noinspection PyTypeChecker
        return self.__json['default_branch']['name']

    @property
    def default_branch_href(self) -> str:
        # noinspection PyTypeChecker
        href = self.__json['default_branch']['@href']
        return f'{BASE_URL}{href}'

    @property
    def builds_href(self) -> str:
        # noinspection PyTypeChecker
        href = f"""{self.__json['@href']}/builds"""
        return f'{BASE_URL}{href}'
