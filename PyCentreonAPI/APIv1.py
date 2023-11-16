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

    try:
        token = response.json()["authToken"]
    except TypeError:
        raise APITokenException("Authentication failed!")

    global v1_api_token, v1_server_url
    v1_api_token = token
    v1_server_url = url
    return token

#todo: finish
def get_hostgroup(host: str = None, service: str = None):
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
                         data=json.dumps(payload), headers=c_header).json()


def get_services(host: str = None, service: str = None):
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
                         data=json.dumps(payload), headers=c_header).json()


def get_service_macro(host: str, service: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "getmacro",
        "object": "SERVICE",
        "values": "{host};{service}".format(host=host, service=service)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def set_service_macro(host: str, service: str, macro_name: str, macro_value: str, macro_description: str, is_password: bool = False):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setmacro",
        "object": "SERVICE",
        "values": "{host};{service};{mname};{mvalue};{ispwd};{descr}".format(host=host, service=service, mname=macro_name, mvalue=macro_value, ispwd=int(is_password), descr=macro_description)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def set_service_param(host: str, service: str, parameter: str, value: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "SERVICE",
        "values": "{host};{service};{param};{val}".format(host=host, service=service, param=parameter, val=value)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def add_service(host: str, service: str, service_template: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "add",
        "object": "SERVICE",
        "values": "{host};{service};{template}".format(host=host, service=service, template=service_template)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def rename_service(host: str, old_name: str, new_name: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "SERVICE",
        "values": "{host};{old_name};description;{new_name}".format(host=host, old_name=old_name, new_name=new_name)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def disable_service(host: str, service: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "SERVICE",
        "values": "{host};{service};activate;0".format(host=host, service=service)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def activate_service(host: str, service: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "SERVICE",
        "values": "{host};{service};activate;1".format(host=host, service=service)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def set_host_param(host: str, parameter: str, value: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "HOST",
        "values": "{host};{param};{val}".format(host=host, param=parameter, val=value)
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()


def get_all_contacts():
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "show",
        "object": "CONTACT"
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()

def add_instance(name: str, address: str, ssh_port: int, gorgone_com_type: int, gorgone_com_port: int):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "add",
        "object": "INSTANCE",
        "values": f"{name};{address};{ssh_port};{gorgone_com_type};{gorgone_com_port}"
    }

    return requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                         data=json.dumps(payload), headers=c_header).json()
