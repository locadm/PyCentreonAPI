import json
import requests
from exceptions import APITokenException

PAGE_SUB1 = "Page argument cannot be lower than 1!"

v2_api_token = None
v2_server_url = None
web_version = None


def check_token():
    global v2_api_token, v2_server_url

    if v2_server_url is None:
        raise APITokenException("Centreon APIv2 server URL not present!")
    if v2_api_token is None:
        raise APITokenException("Centreon APIv2 token not present! Please use authenticate function to obtain API key!")


def authenticate(url: str, username: str, password: str) -> str:
    auth = {"security": {"credentials": {"login": username, "password": password}}}
    response = requests.post("{}/centreon/api/beta/login".format(url), data=json.dumps(auth)).json()
    token = response["security"]["token"]

    response = requests.get("{}/centreon/api/beta/platform/versions".format(url)).json()
    version = response["web"]
    
    global v2_api_token, v2_server_url, web_version
    v2_api_token = token
    v2_server_url = url
    web_version = version

    return token


def get_hosts(search: str = None, limit: int = None, show_service: bool = None, page: int = None,
              verify_ssl: bool = True):
    check_token()

    params = {}

    if limit is not None:
        params["limit"] = limit
    if show_service is not None:
        params["show_service"] = str(show_service).lower()
    if page is not None and page < 1:
        if page < 1:
            raise ValueError(PAGE_SUB1)
        params["page"] = page

    if search is not None:
        params["search"] = search

    global v2_server_url, v2_api_token
    result = requests.get("{}/centreon/api/beta/monitoring/hosts".format(v2_server_url),
                          headers={"X-AUTH-TOKEN": v2_api_token}, verify=verify_ssl, params=params)
    return result.json()


def get_host_groups(search: str = None, limit: int = None, show_host: bool = None,
                    show_service: bool = None, page: int = None, verify_ssl: bool = True):
    check_token()

    params = {}
    if limit is not None:
        params["limit"] = limit
    if show_service is not None:
        params["show_service"] = str(show_service).lower()
    if show_host is not None:
        params["show_host"] = str(show_host).lower()
    if page is not None:
        if page < 1:
            raise ValueError(PAGE_SUB1)
        params["page"] = page

    if search is not None:
        params["search"] = search

    global v2_server_url, v2_api_token
    result = requests.get("{}/centreon/api/beta/monitoring/hostgroups".format(v2_server_url),
                          headers={"X-AUTH-TOKEN": v2_api_token}, verify=verify_ssl, params=params)
    return result.json()


def get_pollers(search: str = None, limit: int = None, page: int = None, verify_ssl: bool = True):
    check_token()

    params = {}
    if limit is not None:
        params["limit"] = limit
    if page is not None:
        if page < 1:
            raise ValueError(PAGE_SUB1)
        params["page"] = page

    if search is not None:
        params["search"] = search

    global v2_server_url, v2_api_token
    result = requests.get("{}/centreon/api/beta/monitoring/servers".format(v2_server_url),
                          headers={"X-AUTH-TOKEN": v2_api_token}, verify=verify_ssl, params=params)
    return result.json()
