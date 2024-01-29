import json
import requests
from . import pcc_exceptions
from . import pcc_enums


class CentreonAPIv1:
    def __init__(self, centreon_url):
        self.__v1_server_url = centreon_url
        self.__v1_api_token = None

    def __check_token(self) -> bool:
        if self.__v1_server_url is None:
            raise pcc_exceptions.APITokenException("Centreon APIv1 server URL not present!")
        if self.__v1_api_token is None:
            raise pcc_exceptions.APITokenException("Centreon APIv1 token not present! "
                                                   "Please use authenticate function to obtain API key!")
        return True

    @staticmethod
    def __check_api_response(api_response: requests.Response) -> bool:
        if api_response.status_code >= 400:
            raise pcc_exceptions.CentreonRequestException(
                f"[HTTP Response {api_response.status_code}] {api_response.content.decode('utf-8')}")
        return True

    @staticmethod
    def __build_payload(obj: str, action: str, values: str = None) -> json:
        payload = {
            "action": action,
            "object": obj,
        }
        if values is not None:
            payload["values"] = values

        return payload

    def __send_request(self, payload: json) -> requests.Response:

        c_header = {
            "Content-Type": "application/json",
            "centreon-auth-token": self.__v1_api_token
        }
        response = requests.post(f"{self.__v1_server_url}/centreon/api/index.php?action=action&object=centreon_clapi",
                                 data=json.dumps(payload), headers=c_header)
        self.__check_api_response(response)
        return response

    def authenticate(self, username: str, password: str) -> str:
        auth = {"username": username, "password": password}
        try:
            response = requests.post(f"{self.__v1_server_url}/centreon/api/index.php?action=authenticate", data=auth)
        except requests.exceptions.ConnectionError:
            raise pcc_exceptions.CentreonConnectionException("Failed to connect to Centreon server!")

        try:
            token = response.json()["authToken"]
        except TypeError:
            raise pcc_exceptions.APITokenException("Authentication failed!")

        self.__v1_api_token = token
        return token

    def get_hosts(self, name: str = None):
        payload = self.__build_payload(obj="HOST", action="show", values=name) if name is not None \
            else self.__build_payload(obj="HOST", action="show")

        response = self.__send_request(payload=payload)
        return response

    def add_host(self, name: str, alias: str, ip: str, poller_name: str, templates: list[str] = None,
                 hostgroups: list[str] = None):
        self.__check_token()

        templates = "|".join(templates) if templates is not None else ""
        hostgroups = "|".join(hostgroups) if hostgroups is not None else ""

        payload = self.__build_payload(obj="HOST", action="add",
                                       values=f"{name};{alias};{ip};{templates};{poller_name};{hostgroups}")
        response = self.__send_request(payload=payload)
        return response

    def set_host_parameter(self, host: str, parameter: pcc_enums.HostParameters, value: str):
        self.__check_token()

        payload = self.__build_payload(obj="HOST", action="setparam", values=f"{host};{parameter};{value}")
        response = self.__send_request(payload=payload)
        return response

    def set_host_macro(self, host: str, macro_name: str, macro_value: str, macro_description: str,
                       is_password: bool = False):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE",
                                       action="setmacro",
                                       values=f"{host};{macro_name};{macro_value};"
                                              f"{int(is_password)};{macro_description}")
        response = self.__send_request(payload=payload)
        return response

    def add_host_template(self, host: str, template: str):
        self.__check_token()

        payload = self.__build_payload(obj="HOST", action="addtemplate", values=f"{host};{template}")
        response = self.__send_request(payload=payload)
        return response

    def add_host_hostgroup(self, host: str, hostgroup: str):
        self.__check_token()

        payload = self.__build_payload(obj="HOST", action="addhostgroup", values=f"{host};{hostgroup}")
        response = self.__send_request(payload=payload)
        return response

    def remove_host_hostgroup(self, host: str, hostgroup: str):
        self.__check_token()

        payload = self.__build_payload(obj="HOST", action="delhostgroup", values=f"{host};{hostgroup}")
        response = self.__send_request(payload=payload)
        return response

    def host_apply_template(self, host: str):
        self.__check_token()

        payload = self.__build_payload(obj="HOST", action="applytpl", values=f"{host}")
        response = self.__send_request(payload=payload)
        return response

    def get_hostgroups(self):
        self.__check_token()

        payload = self.__build_payload(obj="HG", action="show")
        response = self.__send_request(payload=payload)
        return response

    def get_services(self, host: str = None, service: str = None):
        self.__check_token()

        if host is not None or service is not None:
            host = "" if host is None else host
            service = "" if service is None else service
            payload = self.__build_payload(obj="SERVICE", action="show", values=f"{host};{service}")
        else:
            payload = self.__build_payload(obj="SERVICE", action="show")

        response = self.__send_request(payload=payload)
        return response

    def get_service_macro(self, host: str, service: str):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE", action="getmacro", values=f"{host};{service}")
        response = self.__send_request(payload=payload)
        return response

    def set_service_macro(self, host: str, service: str, macro_name: str, macro_value: str, macro_description: str,
                          is_password: bool = False):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE", action="setmacro",
                                       values=f"{host};{service};{macro_name};"
                                              f"{macro_value};{int(is_password)};{macro_description}")
        response = self.__send_request(payload=payload)
        return response

    def set_service_param(self, host: str, service: str, parameter: pcc_enums.ServiceParameters, value: str):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE", action="setparam", values=f"{host};{service};{parameter};{value}")
        response = self.__send_request(payload=payload)
        return response

    def add_service(self, host: str, service: str, service_template: str):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE", action="add", values=f"{host};{service};{service_template}")
        response = self.__send_request(payload=payload)
        return response

    def rename_service(self, host: str, old_name: str, new_name: str):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE", action="setparam",
                                       values=f"{host};{old_name};description;{new_name}")
        response = self.__send_request(payload=payload)
        return response

    def disable_service(self, host: str, service: str):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE", action="setparam", values=f"{host};{service};activate;0")
        response = self.__send_request(payload=payload)
        return response

    def activate_service(self, host: str, service: str):
        self.__check_token()

        payload = self.__build_payload(obj="SERVICE", action="setparam", values=f"{host};{service};activate;1")
        response = self.__send_request(payload=payload)
        return response

    def get_all_contacts(self):
        self.__check_token()

        payload = self.__build_payload(obj="CONTACT", action="show")
        response = self.__send_request(payload=payload)
        return response

    def add_instance(self, name: str, address: str, ssh_port: int, gorgone_com_type: pcc_enums.GorgoneCommType,
                     gorgone_com_port: int):
        self.__check_token()

        payload = self.__build_payload(obj="INSTANCE", action="add",
                                       values=f"{name};{address};{ssh_port};{gorgone_com_type};{gorgone_com_port}")
        response = self.__send_request(payload=payload)
        return response

    def set_instance_param(self, instance: str, param_name: pcc_enums.PollerParameters, param_value: str):
        self.__check_token()

        payload = self.__build_payload(obj="INSTANCE", action="setparam", values=f"{instance};{param_name};{param_value}")
        response = self.__send_request(payload=payload)
        return response

    def add_centengine(self, name: str, instance_name: str, comment: str):
        self.__check_token()

        payload = self.__build_payload(obj="ENGINECFG", action="add", values=f"{name};{instance_name};{comment}")
        response = self.__send_request(payload=payload)
        return response

    def add_broker(self, name: str, instance_name: str):
        self.__check_token()

        payload = self.__build_payload(obj="CENTBROKERCFG", action="add", values=f"{name};{instance_name}")
        response = self.__send_request(payload=payload)
        return response

    def set_centengine_param(self, engine: str, param_name: str, param_value: str):
        self.__check_token()

        payload = self.__build_payload(obj="ENGINECFG", action="setparam", values=f"{engine};{param_name};{param_value}")
        response = self.__send_request(payload=payload)
        return response

    def set_broker_param(self, broker: str, param_name: str, param_value: str):
        self.__check_token()

        payload = self.__build_payload(obj="CENTBROKERCFG", action="setparam",
                                       values=f"{broker};{param_name};{param_value}")
        response = self.__send_request(payload=payload)
        return response
