import datetime
import requests

from Configuration import BASE_URL, DATETIME_ISO_FORMAT, DATETIME_ISO_FORMAT_MS, HEADERS


class TravisJob:
    __json: str
    __start: datetime.datetime
    __end: datetime.datetime

    def __init__(self, job_id):
        self.__json = requests.get(f'{BASE_URL}/job/{job_id}', headers=HEADERS).json()
        self.__start = self.start
        self.__end = self.end

    @property
    def id(self) -> int:
        # noinspection PyTypeChecker
        return int(self.__json['id'])

    @property
    def number(self) -> int:
        # noinspection PyTypeChecker
        return int(self.__json['number'].split('.')[0])

    @property
    def seq_id(self) -> int:
        # noinspection PyTypeChecker
        return int(self.__json['number'].split('.')[1])

    @property
    def created(self) -> datetime.datetime:
        # noinspection PyTypeChecker
        return datetime.datetime.strptime(self.__json['created_at'], DATETIME_ISO_FORMAT_MS)

    @property
    def start(self) -> datetime.datetime:
        # noinspection PyTypeChecker
        return datetime.datetime.strptime(self.__json['started_at'], DATETIME_ISO_FORMAT)

    @property
    def end(self) -> datetime.datetime:
        # noinspection PyTypeChecker
        return datetime.datetime.strptime(self.__json['finished_at'], DATETIME_ISO_FORMAT)

    @property
    def duration(self) -> datetime.timedelta:
        return self.end - self.start

    def duration_seconds(self) -> int:
        return int(self.duration.total_seconds())

    @property
    def state(self) -> str:
        # noinspection PyTypeChecker
        return self.__json['state']
