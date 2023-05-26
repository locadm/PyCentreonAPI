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


def get_hosts(name=None, address=None, regex=None, limit=2147483647, show_service=False):
    check_token()
    params = {"limit": limit, "show_service": show_service}

    if name is not None or address is not None or regex is not None:
        if name is not None:
            params["search"] = '{{"host.name":"{host_name}"}}'.format(host_name=name)
        elif address is not None:
            params["search"] = '{{"host.address":"{host_address}"}}'.format(host_address=address)
        elif regex is not None:
            params["search"] = '{{"host.name":{{"$rg":"{host_regex}"}}}}'.format(host_regex=regex)

    global v2_server_url, v2_api_token
    result = requests.get("{}/centreon/api/beta/monitoring/hosts".format(v2_server_url), headers={"X-AUTH-TOKEN": v2_api_token}, verify=False, params=params)
    return result.json()["result"]
