from typing import Dict, Any
from skydive.rest.client import RESTClient


class SkyNetCtxt():
    def __init__(self):
        """
        SkyNetCtxt constructor
        TODO: Accept configuration
        """
        self._rest = RESTClient("localhost:8082")
        self._options = {}

    def rest_cli(self) -> RESTClient:
        """
        Returns the Skydive REST API client
        """
        return self._rest

    def options(self) -> Dict[str, Any]:
        """
        Returns the global configuration dictionary
        """
        return self._options

    def set_option(self, key: str, value: Any) -> None:
        """
        Adds an option to the global dictionary
        """
        self._options[key] = value
