import hashlib


class TravisYamlJob:
    __yaml: str
    __hash: str
    __number: int

    def __init__(self, job_number: int, job_yaml: str):
        self.__yaml = job_yaml
        self.__hash = hashlib.sha256(str(self.__yaml).encode('utf-8')).hexdigest()
        self.__number = job_number

    @property
    def number(self) -> int:
        return self.__number

    @property
    def hash(self) -> str:
        return self.__hash

    @property
    def yaml(self) -> str:
        return self.__yaml
