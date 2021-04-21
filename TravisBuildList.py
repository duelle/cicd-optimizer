import requests

from TravisBuild import TravisBuild

from Configuration import BASE_URL, HEADERS


class TravisBuildList:
    __json: str
    __builds: []

    def __init__(self, repository_id: int, successful_only: bool = True, build_count: int = 1,
                 exclude_cancelled: bool = True, exclude_incomplete: bool = True):
        self.__json = requests.get(f'{BASE_URL}/repo/{repository_id}/builds', headers=HEADERS).json()
        self.__builds = TravisBuildList.get_builds(self.__json, successful_only, build_count,
                                                   exclude_cancelled, exclude_incomplete)

    @staticmethod
    def get_builds(json, successful_only: bool, build_count: int, exclude_cancelled: bool, exclude_incomplete: bool):
        build_items = []
        current_json = json

        while len(build_items) < build_count:
            current_builds_json = current_json['builds']
            for build_json in current_builds_json:
                if successful_only and build_json['state'] != 'passed':
                    continue
                elif exclude_cancelled and build_json['state'] == 'canceled':
                    continue
                else:
                    current_build = TravisBuild(build_json)
                    if exclude_incomplete and not current_build.is_complete:
                        continue
                    build_items.append(current_build)
            next_href = json['@pagination']['next']['@href']

            # Check if there is a next page
            if next_href != 'null':
                current_json = requests.get(f"""{BASE_URL}{next_href}""", headers=HEADERS).json()
            else:
                break
        return build_items[:build_count]

    @property
    def build_list(self) -> []:
        return self.__builds
