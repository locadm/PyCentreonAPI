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


v1_api_token = None
v1_server_url = None
server_version = None

def check_token():
    global v1_api_token, v1_server_url

    if v1_server_url is None:
        raise APITokenException("Centreon APIv1 server URL not present!")
    if v1_api_token is None:
        raise APITokenException("Centreon APIv1 token not present! Please use authenticate function to obtain API key!")

def authenticate(url: str, username: str, password: str) -> str:
    auth = {"username": username, "password": password}
    response = requests.post("{}/centreon/api/index.php?action=authenticate".format(url), data=auth)

    token = response.json()["authToken"]
    global v1_api_token, v1_server_url
    v1_api_token = token
    v1_server_url = url
    return token


def show_services(host=None, service=None):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "show",
        "object": "SERVICE",
    }
    if host is not None or service is not None:
        if host is None:
            host = ""
        if service is None:
            service = ""
        payload["values"] = ';'.join([host, service])
    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()["result"]
