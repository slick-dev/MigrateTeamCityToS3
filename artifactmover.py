#!/usr/bin/python3
import argparse
import os
from datetime import datetime

import common


def run() -> None:
    args = parse_args()

    local_artifact_root = args.local_artifact_root
    backup_directory = args.backup_directory
    dry_mode = args.dry

    for build_result_dir in common.build_results_iter(local_artifact_root):
        print("{}: Working in {}".format(datetime.now().isoformat(' '), build_result_dir))

        artifact_list = common.get_artifact_list(build_result_dir)
        json_exists = os.path.exists(os.path.join(build_result_dir, '.teamcity', 'artifacts.json'))
        if artifact_list and json_exists:
            for artifact in artifact_list:
                mv(local_artifact_root, backup_directory, artifact, dry_mode)
        elif artifact_list and not json_exists:
            raise Exception('Artifacts exist but no JSON file?! Did you successfully migrate this '
                            'directory to S3? Each directory with artifacts should have a JSON file to go '
                            'along with it, which would have been generated by the awsupload.py script. '
                            + build_result_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--backup-directory', default=common.DEFAULT_ARTIFACT_BACKUP_ROOT, required=True,
                        help='Local directory where old artifacts can be moved. This should be out of the way of '
                             'TeamCity\'s existing artifact root so as to ensure the S3 migration completed '
                             'successfully.')

    common.add_local_artifact_root_argument(parser)
    common.add_dry_mode_argument(parser)

    return parser.parse_args()


def mv(local_artifact_root: str, backup_directory: str, source: str, dry_mode: bool) -> None:
    relative_source = source[len(local_artifact_root):]
    target = backup_directory + relative_source

    print('{0} -> {1}'.format(source, target),flush=True)
    if not dry_mode:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        os.rename(source, target)


if '__main__' == __name__:
    run()
