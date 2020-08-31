#!/usr/bin/python3

import subprocess

lines = subprocess.check_output('aws s3 ls --recursive s3://david-zemon-teamcity-artifacts', shell=True)
lines = lines.decode().split('\n')
for line in lines:
    if line.endswith('.tar.gz'):
        words = line.split()
        artifact = words[3]
        uri = 's3://david-zemon-teamcity-artifacts/' + artifact
        command = [
                'aws', 's3', 'cp',
                '--content-type', 'application/x-gzip',
                uri, uri,
                '--metadata-directive', 'REPLACE'
        ]
        print(' '.join(command))
        subprocess.run(command)
        
#From: https://youtrack.jetbrains.com/issue/TW-52778
