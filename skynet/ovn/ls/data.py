from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata


class LSData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('UUID'),
    ]
    """
    LSData represents Logical Switch Data
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        LSData constructor
        """
        super(LSData, self).__init__(data=data,
                                     meta=self.METADATA,
                                     index="UUID")


class LSProvider():
    """
    LSProvider is a provider for Logical Switches
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LSProvider constructor
        """
        self._ctxt = ctxt

    def get(self) -> LSData:
        data = self._ctxt.rest_cli().lookup(
            "g.V().Has('Type', 'logical_switch')")
        return LSData(data)
