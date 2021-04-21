import requests
import yaml

from TravisYamlJob import TravisYamlJob


class TravisYaml:
    __yaml: str
    __commit: str
    __jobs: []

    def __init__(self, repo_org: str, repo_name: str, commit: str = 'master'):
        travis_url = f'https://github.com/{repo_org}/{repo_name}/raw/{commit}/.travis.yml'
        response = requests.get(travis_url, allow_redirects=True)
        self.__yaml = yaml.load(response.content, Loader=yaml.FullLoader)
        self.__commit = commit
        self.__jobs = []

    def __get_jobs(self) -> []:
        job_list: [] = []
        # noinspection PyTypeChecker
        jobs_yaml: str = self.__yaml['jobs']['include']
        job_number: int = 1
        for job in jobs_yaml:
            current_job = TravisYamlJob(job_number, job)
            job_list.append(current_job)
            job_number += 1
        return job_list

    @property
    def yaml(self) -> str:
        return self.__yaml

    @property
    def commit(self) -> str:
        return self.__commit

    @property
    def jobs(self) -> []:
        if not self.__jobs:
            self.__jobs = self.__get_jobs()
        return self.__jobs

    def get_job_by_number(self, number) -> TravisYamlJob:
        return [x for x in self.jobs if x.number == number][0]

    def rearrange(self, job_order: []):
        jobs_section: [] = []
        for entry in job_order:
            job_yaml = self.get_job_by_number(entry).yaml
            print(job_yaml)
            jobs_section.append(job_yaml)
        # noinspection PyTypeChecker
        self.__yaml['jobs']['include'] = jobs_section
        self.__jobs = None
        return self
