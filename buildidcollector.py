#!/usr/bin/env python3

import yaml
import json
from datetime import timedelta

from TravisRepository import TravisRepository
from TravisBuildList import TravisBuildList
from TravisYaml import TravisYaml

branch = 'master'
repository_org = 'curl'
repository_name = 'curl'
repository_slug = f'{repository_org}%2F{repository_name}'

# travis_yaml = TravisYaml(repository_org, repository_name)
# for x in travis_yaml.jobs:
#    print(x.number, x.hash)

curl_repo = TravisRepository(repository_slug)
curl_repo_id = curl_repo.id
curl_build_list = TravisBuildList(curl_repo_id, successful_only=False, build_count=100, exclude_incomplete=True)
build_list = curl_build_list.build_list
# yaml.Dumper.ignore_aliases = lambda self, data: True
job_order: [] = []
print('build_id, build_number, build_job_start, build_duration_api, build_duration_diff, build_job_end, '
      'build_max_workers, build_trigger, build_state')
for build in build_list:
    # print({build})
    print(f'{build.id}, {build.number}, {build.job_start}, {str(build.duration)}, '
          f'{str(build.job_diff_duration)}, {build.job_end}, '
          f'{build.max_workers}, {build.trigger}, {build.state}')
    #sorted_builds = sorted(build.job_list, key=lambda x: x.duration, reverse=True)
    #for job in sorted_builds:
    #    job_order.append(job.seq_id)
    #    print(f'{job.number}.{job.seq_id}: {job.duration}')

#travis_yaml = TravisYaml("curl", "curl")
#re_travis_yaml = travis_yaml.rearrange(job_order)
#print(re_travis_yaml.yaml)

#with open('/tmp/travis-curl.yaml', 'w') as output:
#    yaml.dump(re_travis_yaml.yaml, output, default_flow_style=False, sort_keys=False)

#with open('/tmp/travis-curlx.yaml', 'w') as output:
#    json_object = json.dumps(re_travis_yaml.yaml, indent=4)
#    output.write(json_object)

    # min_duration = 9999999999
    # max_duration = 0
    # for job in build.job_list:
    #    job_duration = job.duration.total_seconds()
    #    if job_duration > max_duration:
    #        max_duration = job_duration
    #    if job_duration < min_duration:
    #        min_duration = job_duration
    #    print(f'  {job.seq_id} ({job.state}): {job_duration} {job.created} {job.start} {job.end}')
        # print(f'{job_duration},')

    # print(f'{build.id}: {build.end}')
    # print(f'min: {min_duration}, max: {max_duration}, sum: {min_duration + max_duration}')
    # print()
