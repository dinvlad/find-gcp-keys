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


# For requirements on GCP project IDs, see
# https://cloud.google.com/resource-manager/docs/creating-managing-projects
PROJECT_PATTERN = r"[a-z][a-z0-9\-]{4,28}[a-z0-9]"
FILE_PATTERN = re.compile(PROJECT_PATTERN + r"-[0-9a-f]{12}\.json")


def find_key_paths(dir_path: str):
    """ Finds files whose name matches the JSON SA key pattern """
    for dirpath, _, files in os.walk(dir_path):
        for file in files:
            if FILE_PATTERN.match(file):
                yield os.path.join(dirpath, file)


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
