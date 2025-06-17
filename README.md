# PyCentreonAPI

PyCentreonAPI is a simple Python wrapper around the Centreon REST API. It
supports the legacy API v1 as well as the newer API v2, allowing you to
manage hosts, services, contact groups and more from your own scripts.

## Installation

The project does not ship a standalone command line tool. To install the
library, clone this repository and install it with `pip`:

```bash
pip install .
```

The only runtime dependency is `requests`.

## Usage

### API v1

```python
from PyCentreonAPI import CentreonAPIv1

api = CentreonAPIv1("https://centreon.example.com")
api.authenticate("my_user", "my_password")

# List all hosts
hosts_response = api.get_hosts()
print(hosts_response.json())
```

### API v2

```python
from PyCentreonAPI import CentreonAPIv2

api = CentreonAPIv2("https://centreon.example.com")
api.authenticate("my_user", "my_password")

# Search for hosts
hosts = api.get_hosts(search="srv", limit=10)
print(hosts)
```

Refer to the available methods in `APIv1.py` and `APIv2.py` for the
complete list of operations.

## Development

This repository contains only the library code. No additional setup is
required besides installing the dependencies. Examples above should help
get you started interacting with your Centreon instance.
