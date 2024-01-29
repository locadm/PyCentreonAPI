import json
import requests
from exceptions import CentreonRequestException, APITokenException, CentreonConnectionException

v1_api_token = None
v1_server_url = None
server_version = None


def check_token() -> bool:
    global v1_api_token, v1_server_url

    if v1_server_url is None:
        raise APITokenException("Centreon APIv1 server URL not present!")
    if v1_api_token is None:
        raise APITokenException("Centreon APIv1 token not present! Please use authenticate function to obtain API key!")
    return True


def check_api_response(api_response: requests.Response) -> bool:
    if api_response.status_code >= 400:
        raise CentreonRequestException(
            f"[HTTP Response {api_response.status_code}] {api_response.content.decode('utf-8')}")
    return True


def build_payload(obj: str, action: str, values: str = None) -> json:
    payload = {
        "action": action,
        "object": obj,
    }
    if values is not None:
        payload["values"] = values

    return payload


def send_request(payload: json) -> requests.Response:
    global v1_api_token, v1_server_url

    c_header = {
        "Content-Type": "application/json",
        "centreon-auth-token": v1_api_token
    }
    response = requests.post(f"{v1_server_url}/centreon/api/index.php?action=action&object=centreon_clapi",
                             data=json.dumps(payload), headers=c_header)
    check_api_response(response)
    return response


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


def get_hosts(name: str = None):
    if name is not None:
        payload = build_payload(obj="HOST", action="show", values=name)
    else:
        payload = build_payload(obj="HOST", action="show")

    response = send_request(payload=payload)
    return response


def add_host(name: str, alias: str, ip: str, poller_name: str, templates: list[str] = None,
             hostgroups: list[str] = None):
    check_token()

    templates = "|".join(templates) if templates is not None else ""
    hostgroups = "|".join(hostgroups) if hostgroups is not None else ""

    payload = build_payload(obj="HOST",
                            action="add",
                            values=f"{name};{alias};{ip};{templates};{poller_name};{hostgroups}")
    response = send_request(payload=payload)
    return response


def set_host_param(host: str, parameter: str, value: str):
    check_token()

    payload = build_payload(obj="HOST",
                            action="setparam",
                            values=f"{host};{parameter};{value}")
    response = send_request(payload=payload)
    return response


def set_host_macro(host: str, macro_name: str, macro_value: str, macro_description: str, is_password: bool = False):
    check_token()

    payload = build_payload(obj="SERVICE",
                            action="setmacro",
                            values=f"{host};{macro_name};{macro_value};{int(is_password)};{macro_description}")
    response = send_request(payload=payload)
    return response


def add_host_template(host: str, template: str):
    check_token()

    payload = build_payload(obj="HOST", action="addtemplate", values=f"{host};{template}")
    response = send_request(payload=payload)
    return response


def add_host_hostgroup(host: str, hostgroup: str):
    check_token()

    payload = build_payload(obj="HOST", action="addhostgroup", values=f"{host};{hostgroup}")
    response = send_request(payload=payload)
    return response


def remove_host_hostgroup(host: str, hostgroup: str):
    check_token()

    payload = build_payload(obj="HOST", action="delhostgroup", values=f"{host};{hostgroup}")
    response = send_request(payload=payload)
    return response


def host_apply_template(host: str):
    check_token()

    payload = build_payload(obj="HOST", action="applytpl", values=f"{host}")
    response = send_request(payload=payload)
    return response


def get_hostgroups():
    check_token()

    payload = build_payload(obj="HG", action="show")
    response = send_request(payload=payload)
    return response


def get_services(host: str = None, service: str = None):
    check_token()

    if host is not None or service is not None:
        host = "" if host is None else host
        service = "" if service is None else service
        payload = build_payload(obj="SERVICE", action="show", values=f"{host};{service}")
    else:
        payload = build_payload(obj="SERVICE", action="show")

    response = send_request(payload=payload)
    return response


def get_service_macro(host: str, service: str):
    check_token()

    payload = build_payload(obj="SERVICE", action="getmacro", values=f"{host};{service}")
    response = send_request(payload=payload)
    return response


def set_service_macro(host: str, service: str, macro_name: str, macro_value: str, macro_description: str,
                      is_password: bool = False):
    check_token()

    payload = build_payload(obj="SERVICE", action="setmacro",
                            values=f"{host};{service};{macro_name};"
                                   f"{macro_value};{int(is_password)};{macro_description}")
    response = send_request(payload=payload)
    return response


def set_service_param(host: str, service: str, parameter: str, value: str):
    check_token()

    payload = build_payload(obj="SERVICE", action="setparam", values=f"{host};{service};{parameter};{value}")
    response = send_request(payload=payload)
    return response


def add_service(host: str, service: str, service_template: str):
    check_token()

    payload = build_payload(obj="SERVICE", action="add", values=f"{host};{service};{service_template}")
    response = send_request(payload=payload)
    return response


def rename_service(host: str, old_name: str, new_name: str):
    check_token()

    payload = build_payload(obj="SERVICE", action="setparam", values=f"{host};{old_name};description;{new_name}")
    response = send_request(payload=payload)
    return response


def disable_service(host: str, service: str):
    check_token()

    payload = build_payload(obj="SERVICE", action="setparam", values=f"{host};{service};activate;0")
    response = send_request(payload=payload)
    return response


def activate_service(host: str, service: str):
    check_token()

    payload = build_payload(obj="SERVICE", action="setparam", values=f"{host};{service};activate;1")
    response = send_request(payload=payload)
    return response


def get_all_contacts():
    check_token()

    payload = build_payload(obj="CONTACT", action="show")
    response = send_request(payload=payload)
    return response


def add_instance(name: str, address: str, ssh_port: int, gorgone_com_type: int, gorgone_com_port: int):
    check_token()

    payload = build_payload(obj="INSTANCE", action="add",
                            values=f"{name};{address};{ssh_port};{gorgone_com_type};{gorgone_com_port}")
    response = send_request(payload=payload)
    return response


def set_instance_param(instance: str, param_name: str, param_value: str):
    check_token()

    payload = build_payload(obj="INSTANCE", action="setparam", values=f"{instance};{param_name};{param_value}")
    response = send_request(payload=payload)
    return response


def add_centengine(name: str, instance_name: str, comment: str):
    check_token()

    payload = build_payload(obj="ENGINECFG", action="add", values=f"{name};{instance_name};{comment}")
    response = send_request(payload=payload)
    return response


def add_broker(name: str, instance_name: str):
    check_token()

    payload = build_payload(obj="CENTBROKERCFG", action="add", values=f"{name};{instance_name}")
    response = send_request(payload=payload)
    return response


def set_centengine_param(engine: str, param_name: str, param_value: str):
    check_token()

    payload = build_payload(obj="ENGINECFG", action="setparam", values=f"{engine};{param_name};{param_value}")
    response = send_request(payload=payload)
    return response


def set_broker_param(broker: str, param_name: str, param_value: str):
    check_token()

    payload = build_payload(obj="CENTBROKERCFG", action="setparam", values=f"{broker};{param_name};{param_value}")
    response = send_request(payload=payload)
    return response
