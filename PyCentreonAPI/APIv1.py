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


class CentreonConnectionException(Exception):
    """Exception raised when connection to Centreon fails

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Exception raised when unable to connect to server"):
        self.message = message
        super().__init__(self.message)


class CentreonRequestException(Exception):
    """Exception raised when Centreon API returns an error

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Exception raised when API error encountered"):
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


def check_api_response(api_response: requests.Response):
    if api_response.status_code >= 400:
        raise CentreonRequestException(
            f"[HTTP Response {api_response.status_code}] {api_response.content.decode('utf-8')}")


def authenticate(url: str, username: str, password: str) -> str:
    auth = {"username": username, "password": password}
    try:
        response = requests.post("{}/centreon/api/index.php?action=authenticate".format(url), data=auth)
    except requests.exceptions.ConnectionError:
        raise CentreonConnectionException("Failed to connect to Centreon server!")

    try:
        token = response.json()["authToken"]
    except TypeError:
        raise APITokenException("Authentication failed!")

    global v1_api_token, v1_server_url
    v1_api_token = token
    v1_server_url = url
    return token


def get_hosts(name = None):
    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "show",
        "object": "HOST",
    }
    if name is not None:
        payload["values"] = name

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response

def add_host(name: str, alias: str, ip: str, poller_name: str, templates: list[str] = None,
             hostgroups: list[str] = None):
    if templates is None:
        templates = [""]
    global v1_api_token, v1_server_url
    check_token()

    if templates is not None and len(templates) > 0:
        templates = "|".join(templates)
    else:
        templates = ""

    if hostgroups is not None and len(hostgroups) > 0:
        hostgroups = "|".join(hostgroups)
    else:
        hostgroups = ""

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "add",
        "object": "HOST",
        "values": f"{name};{alias};{ip};{templates};{poller_name};{hostgroups}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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
        "values": f"{host};{parameter};{value}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def set_host_macro(host: str, macro_name: str, macro_value: str, macro_description: str, is_password: bool = False):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setmacro",
        "object": "SERVICE",
        "values": f"{host};{macro_name};{macro_value};{int(is_password)};{macro_description}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def add_host_template(host: str, template: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "addtemplate",
        "object": "HOST",
        "values": f"{host};{template}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def host_apply_template(host: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "applytpl",
        "object": "HOST",
        "values": f"{host}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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
    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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
    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def set_service_macro(host: str, service: str, macro_name: str, macro_value: str, macro_description: str,
                      is_password: bool = False):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setmacro",
        "object": "SERVICE",
        "values": "{host};{service};{mname};{mvalue};{ispwd};{descr}".format(host=host, service=service,
                                                                             mname=macro_name, mvalue=macro_value,
                                                                             ispwd=int(is_password),
                                                                             descr=macro_description)
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def set_instance_param(instance: str, param_name: str, param_value: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "INSTANCE",
        "values": f"{instance};{param_name};{param_value}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def add_centengine(name: str, instance_name: str, comment: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "add",
        "object": "ENGINECFG",
        "values": f"{name};{instance_name};{comment}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def add_broker(name: str, instance_name: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "add",
        "object": "CENTBROKERCFG",
        "values": f"{name};{instance_name}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def set_centengine_param(engine: str, param_name: str, param_value: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "ENGINECFG",
        "values": f"{engine};{param_name};{param_value}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


def set_broker_param(broker: str, param_name: str, param_value: str):
    global v1_api_token, v1_server_url
    check_token()

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    payload = {
        "action": "setparam",
        "object": "CENTBROKERCFG",
        "values": f"{broker};{param_name};{param_value}"
    }

    response = requests.post("{}/centreon/api/index.php?action=action&object=centreon_clapi".format(v1_server_url),
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response
