#!/usr/bin/env python3
"""
Finds and reports valid Google Service Account keys on your filesystem
"""

import argparse
import os
import re
import sys

import google.auth.transport.requests
from google.oauth2 import service_account


def parse_args():
    """ Parses command-line args """

    parser = argparse.ArgumentParser(
        description='Find and report valid Google Service Account keys on your filesystem',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        dest='dir_path', help='Directory path to search recursively',
    )
    return parser.parse_args()


def find_key_paths(dir_path: str):
    """ Finds files whose name matches the JSON SA key pattern """

    # For requirements on GCP project IDs, see
    # https://cloud.google.com/resource-manager/docs/creating-managing-projects
    project_pattern = r"[a-z][a-z0-9\-]{4,28}[a-z0-9]"
    file_pattern = re.compile(project_pattern + r"-[0-9a-f]{12}\.json")

    with os.scandir(dir_path) as dir_iter:
        for file in dir_iter:
            if file_pattern.match(file.name):
                yield file.path


def is_valid_key(file_path: str):
    """ Checks if the key is still valid in GCP """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            file_path, scopes=["openid"],
        )
        credentials.refresh(google.auth.transport.requests.Request())
        return True
    except (ValueError, google.auth.exceptions.RefreshError):
        return False


def main():
    """ Main entrypoint """
    args = parse_args()

    found = False
    for path in find_key_paths(args.dir_path):
        if is_valid_key(path):
            print(path, file=sys.stderr)
            found = True

    if found:
        sys.exit(1)


if __name__ == "__main__":
    main()
