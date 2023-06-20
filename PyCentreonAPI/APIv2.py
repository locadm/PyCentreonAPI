import json
import requests


class APITokenException(Exception):
    """Exception raised when token fails

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="Exception raised when token does not exist"):
        self.message = message
        super().__init__(self.message)


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


def get_hosts(name: str = None, address: str = None, regex: str = None, custom_search: str = None, limit: int = None, show_service: bool = None, page: int = None):
    check_token()

    n_exclusive = 0
    args = locals()

    for k in list(args.keys())[:4]:
        if args[k] is not None:
            n_exclusive += 1

    if n_exclusive > 1:
        raise ValueError('Arguments "name", "address", "regex" and "custom_search" cannot be used multiple at the '
                         'same time! For more complicated queries use custom search only!')

    params = {}
    if limit is not None:
        params["limit"] = limit
    if show_service is not None:
        params["show_service"] = str(show_service).lower()
    if page is not None:
        if page < 1:
            raise ValueError("Page argument cannot be lower than 1!")
        params["page"] = page

    if name is not None or address is not None or regex is not None or custom_search is not None:
        if name is not None:
            params["search"] = '{{"host.name":"{host_name}"}}'.format(host_name=name)
        elif address is not None:
            params["search"] = '{{"host.address":"{host_address}"}}'.format(host_address=address)
        elif regex is not None:
            params["search"] = '{{"host.name":{{"$rg":"{host_regex}"}}}}'.format(host_regex=regex)
        elif custom_search is not None:
            params["search"] = custom_search

    global v2_server_url, v2_api_token
    result = requests.get("{}/centreon/api/beta/monitoring/hosts".format(v2_server_url), headers={"X-AUTH-TOKEN": v2_api_token}, verify=False, params=params)
    return result.json()


# TODO: group_id doesn't work/ BUG??? WHY???
def get_host_groups(group_id: int = None, child_host_id: int = None, custom_search: str = None, limit: int = None, show_host: bool = None, show_service: bool = None, page: int = None):
    check_token()

    n_exclusive = 0
    args = locals()

    for k in list(args.keys())[:3]:
        if args[k] is not None:
            n_exclusive += 1

    if n_exclusive > 1:
        raise ValueError('Arguments "group_name", "group_id", "regex" and "custom_search" cannot be used simultaneously! '
                         'For more complicated queries use custom_search only!')

    params = {}
    if limit is not None:
        params["limit"] = limit
    if show_service is not None:
        params["show_service"] = str(show_service).lower()
    if show_host is not None:
        params["show_host"] = str(show_host).lower()
    if page is not None:
        if page < 1:
            raise ValueError("Page argument cannot be lower than 1!")
        params["page"] = page

    if group_id is not None or custom_search is not None or child_host_id is not None:
        if group_id is not None:
            params["search"] = '{{"host_group.id":"{id}"}}'.format(id=group_id)
        elif child_host_id is not None:
            params["search"] = '{{"host.id":"{id}"}}'.format(id=child_host_id)
        elif custom_search is not None:
            params["search"] = custom_search

    global v2_server_url, v2_api_token
    result = requests.get("{}/centreon/api/beta/monitoring/hostgroups".format(v2_server_url), headers={"X-AUTH-TOKEN": v2_api_token}, verify=False, params=params)
    return result.json()


def get_pollers(poller_id: int = None, poller_name: str = None, custom_search: str = None, limit: int = None, page: int = None):
    check_token()

    n_exclusive = 0
    args = locals()

    for k in list(args.keys())[:2]:
        if args[k] is not None:
            n_exclusive += 1

    if n_exclusive > 1:
        raise ValueError('Arguments "group_name", "group_id", "regex" and "custom_search" cannot be used simultaneously! '
                         'For more complicated queries use custom_search only!')

    params = {}
    if limit is not None:
        params["limit"] = limit
    if page is not None:
        if page < 1:
            raise ValueError("Page argument cannot be lower than 1!")
        params["page"] = page

    if poller_id is not None or custom_search is not None or poller_name is not None:
        if poller_id is not None:
            params["search"] = '{{"id":"{id}"}}'.format(id=poller_id)
        elif poller_name is not None:
            params["search"] = '{{"name":"{id}"}}'.format(id=poller_name)
        elif custom_search is not None:
            params["search"] = custom_search

    global v2_server_url, v2_api_token
    result = requests.get("{}/centreon/api/beta/monitoring/servers".format(v2_server_url), headers={"X-AUTH-TOKEN": v2_api_token}, verify=False, params=params)
    return result.json()