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
        dest='dir_path',
        help='Directory path to search recursively',
    )
    parser.add_argument(
        '--no-validate', '-n', action='store_true',
        help='Directory path to search recursively',
    )
    parser.add_argument(
        '--file-pattern', '-p', default=PROJECT_JSON_PATTERN,
        help='Pattern to match JSON file names against',
    )
    return parser.parse_args()


# For requirements on GCP project IDs, see
# https://cloud.google.com/resource-manager/docs/creating-managing-projects
PROJECT_PATTERN = r"[a-z][a-z0-9\-]{4,28}[a-z0-9]"
PROJECT_JSON_PATTERN = PROJECT_PATTERN + r"-[0-9a-f]{12}\.json"


def find_key_paths(dir_path: str, file_pattern: str):
    """ Finds files whose name matches `file_pattern` """
    file_re = re.compile(file_pattern)
    for dirpath, _, files in os.walk(dir_path):
        for file in files:
            if file_re.match(file):
                yield os.path.join(dirpath, file)


def is_valid_key(file_path: str):
    """ Checks if the key is still valid in GCP """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            file_path, scopes=["openid"],
        )
        credentials.refresh(google.auth.transport.requests.Request())
        return True
    except (AttributeError, ValueError, google.auth.exceptions.RefreshError):
        return False


def find_valid_keys(dir_path: str, file_pattern: str):
    """ Recursively walks `dir_path` and finds valid GCP SA keys """
    for path in find_key_paths(dir_path, file_pattern):
        if is_valid_key(path):
            yield path


def main():
    """ Main entrypoint """
    args = parse_args()

    if args.no_validate:
        for path in find_key_paths(args.dir_path, args.file_pattern):
            print(path)
        sys.exit(0)

    found = False
    for path in find_valid_keys(args.dir_path, args.file_pattern):
        print(path, file=sys.stderr)
        found = True

    if found:
        sys.exit(1)


if __name__ == "__main__":
    main()
