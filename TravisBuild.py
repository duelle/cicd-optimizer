import datetime
import typing

from Configuration import DATETIME_ISO_FORMAT
from TravisJob import TravisJob


class TravisBuild:
    __json: str
    __jobs: []
    __max_workers: int
    __job_start: typing.Optional[datetime.datetime] = None
    __job_end: typing.Optional[datetime.datetime] = None
    __duration: typing.Optional[datetime.timedelta] = None

    def __init__(self, build_json):
        self.__json = build_json
        self.__jobs = None
        self.__job_start = None
        self.__job_end = None
        self.__duration = None
        self.__max_workers = 0

    def __repr__(self):
        start_time = "unknown"
        end_time = "unknown"

        try:
            start_time = self.start
            end_time = self.end
        finally:
            return f'{self.id} {self.state}: {start_time} - {end_time} {self.duration} Jobs: {len(self.job_list)}'

    @staticmethod
    def get_jobs(json):
        job_list: [] = []
        jobs = json['jobs']
        for job in jobs:
            job_id = job['id']
            try:
                current_job = TravisJob(job_id)
                job_list.append(current_job)
            except TypeError:
                print(f'Incomplete job data (job_id: {job_id})')
                continue
        return job_list

    @property
    def max_workers(self) -> int:
        max_workers: int = 0
        current_workers: int = 0

        # Sort the jobs by their start time and assign the modifier of "1"
        jobs_start = [(item.start, 1) for item in sorted(self.job_list, key=lambda x: x.start)]

        # Sort the jobs by their end time and assign a modifier of "-1"
        jobs_end = [(item.end, -1) for item in sorted(self.job_list, key=lambda x: x.end)]

        # Combine the lists and order them by the times
        jobs_combined = [item for item in sorted((jobs_start + jobs_end), key=lambda x: x[0])]

        # Loop through combined list and add up the modifiers to determine the maximum number of parallel builds
        for job in jobs_combined:
            current_workers += job[1]
            if current_workers > max_workers:
                max_workers = current_workers
        return max_workers

    @property
    def state(self) -> str:
        # noinspection PyTypeChecker
        return self.__json['state']

    @property
    def id(self) -> int:
        # noinspection PyTypeChecker
        return int(self.__json['id'])

    @property
    def number(self) -> int:
        # noinspection PyTypeChecker
        return int(self.__json['number'])

    @property
    def duration(self) -> datetime.timedelta:
        if not self.__duration:
            self.__duration = (self.end - self.start)
        return self.__duration

    @property
    def duration_seconds(self) -> int:
        return int(self.duration.total_seconds())

    @property
    def processing_time(self) -> int:
        # noinspection PyTypeChecker
        return int(self.__json['duration'])

    @property
    def job_list(self) -> []:
        if not self.__jobs:
            self.__jobs = TravisBuild.get_jobs(self.__json)
        return self.__jobs

    @property
    def queue(self) -> str:
        # noinspection PyTypeChecker
        return self.__json['queue']

    @property
    def start(self) -> datetime.datetime:
        # noinspection PyTypeChecker
        return datetime.datetime.strptime(self.__json['started_at'], DATETIME_ISO_FORMAT)

    @property
    def job_start(self):
        if not self.__job_start:
            self.__job_start = self.__job_start = [item.start for item in
                                                   sorted(self.job_list, key=lambda x: x.start) if item.start][0]
        return self.__job_start

    @property
    def job_end(self):
        if not self.__job_end:
            self.__job_end = [item.end for item in
                              sorted(self.job_list, key=lambda x: x.end, reverse=True) if item.end][0]
        return self.__job_end

    @property
    def end(self) -> datetime.datetime:
        # noinspection PyTypeChecker
        return datetime.datetime.strptime(self.__json['finished_at'], DATETIME_ISO_FORMAT)

    @property
    def trigger(self) -> str:
        # noinspection PyTypeChecker
        return self.__json['event_type']

    @property
    def job_diff_duration(self) -> datetime.timedelta:
        return self.job_end - self.job_start

    @property
    def job_diff_duration_seconds(self) -> int:
        return int(self.job_diff_duration.total_seconds())

    @property
    def is_complete(self):
        try:
            if self.start and self.end:
                return True
            else:
                return False
        # this happens in case start and/or end are not present due to missing time information
        except TypeError:
            return False
