# find-gcp-keys

This tool finds and prints valid Google Service Account keys on your filesystem.
This is useful to keep track of any unexpired/non-disabled keys you may have.

It does NOT require any special permissions,
or even to be authenticated with Google Cloud SDK.

## Requirements

Python 3.7+

## Installation

pip3 install find-gcp-keys

## Usage

As a command-line utility:

```
find_gcp_keys <dir_path>
```

As a library:

```
import find_gcp_keys
...
for path in find_gcp_keys.search(dir_path):
  print(path)
```
