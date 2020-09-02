# find-gcp-keys

This tool finds and prints valid Google Service Account keys on your filesystem.
This is useful for keeping track of any unexpired/non-disabled keys you may have.

It does NOT require any special permissions,
or even to be authenticated with Google Cloud SDK.

## Requirements

Python 3.7+

## Installation

```
pip3 install find-gcp-keys
```

## Usage

As a command-line utility:

```
find-gcp-keys <dir_path>
```

As a library:

```py
from find_gcp_keys import find_key_paths, find_valid_keys, is_valid_key
...

# determine if a given file is a valid key
if is_valid_key(file_path):
  ...

# recursively search for valid keys
for file_path in find_valid_keys(dir_path):
  ...

# recursively search for possible keys, but don't validate them
for file_path in find_key_paths(dir_path):
  ...
```
