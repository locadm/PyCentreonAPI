import json
import requests
from . import pcc_exceptions

PAGE_SUB1 = "Page argument cannot be lower than 1!"


class CentreonAPIv2:
    def __init__(self, centreon_url):
        try:
            status_code = requests.head(centreon_url).status_code
            if status_code >= 400:
                raise pcc_exceptions.CentreonConnectionException(f'Centreon server on following URL: '
                                                                 f'"{centreon_url}" returned code {status_code}')
        except requests.exceptions.ConnectionError:
            raise pcc_exceptions.CentreonConnectionException(f'Failed to request Centreon server on following URL: '
                                                             f'"{centreon_url}"')

        self.__v2_server_url = centreon_url
        self.__v2_api_token = None

    def __check_token(self) -> bool:
        if self.__v2_server_url is None:
            raise pcc_exceptions.APITokenException("Centreon APIv2 server URL not present!")
        if self.__v2_api_token is None:
            raise pcc_exceptions.APITokenException("Centreon APIv2 token not present! "
                                                   "Please use authenticate function to obtain API key!")
        return True

    def authenticate(self, username: str, password: str) -> str:
        auth = {"security": {"credentials": {"login": username, "password": password}}}
        try:
            response = requests.post("{}/centreon/api/beta/login".format(self.__v2_server_url),
                                     data=json.dumps(auth)).json()
        except requests.exceptions.ConnectionError:
            raise pcc_exceptions.CentreonConnectionException("Failed to connect to Centreon server!")

        try:
            token = response["security"]["token"]
        except KeyError:
            raise pcc_exceptions.APITokenException("Authentication failed!")

        self.__v2_api_token = token
        return token

    def get_token(self) -> str:
        return self.__v2_api_token

    def get_hosts(self, search, limit: int = None, show_service: bool = None, page: int = None,
                  verify_ssl: bool = True):
        self.__check_token()

        params = {}

        if limit is not None:
            params["limit"] = limit
        if show_service is not None:
            params["show_service"] = str(show_service).lower()
        if page is not None:
            if page < 1:
                raise ValueError(PAGE_SUB1)
            params["page"] = page

        params["search"] = search

        result = requests.get(f"{self.__v2_server_url}/centreon/api/beta/monitoring/hosts",
                              headers={"X-AUTH-TOKEN": self.__v2_api_token}, verify=verify_ssl, params=params)
        return result.json()

    def get_host_groups(self, search, limit: int = None, show_host: bool = None,
                        show_service: bool = None, page: int = None, verify_ssl: bool = True):
        self.__check_token()

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

        params["search"] = search

        result = requests.get(f"{self.__v2_server_url}/centreon/api/beta/monitoring/hostgroups",
                              headers={"X-AUTH-TOKEN": self.__v2_api_token}, verify=verify_ssl, params=params)
        return result.json()

    def get_pollers(self, search, limit: int = None, page: int = None, verify_ssl: bool = True):
        self.__check_token()

        params = {}
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            if page < 1:
                raise ValueError(PAGE_SUB1)
            params["page"] = page

        params["search"] = search

        result = requests.get(f"{self.__v2_server_url}/centreon/api/beta/monitoring/servers",
                              headers={"X-AUTH-TOKEN": self.__v2_api_token}, verify=verify_ssl, params=params)
        return result.json()
