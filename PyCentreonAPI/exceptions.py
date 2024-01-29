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
