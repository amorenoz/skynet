from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata


class LRData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('UUID'),
        Metadata('Host'),
        Metadata('OVN.ExtID', None, 'ExtID'),
    ]
    """
    LRData represents Logical Router Data
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        LRData constructor
        """
        super(LRData, self).__init__(data=data,
                                     meta=self.METADATA,
                                     index="UUID")


class LRProvider():
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LRProvider constructor
        """
        self._ctxt = ctxt

    def get(self) -> LRData:
        data = self._ctxt.rest_cli().lookup(
            "g.V().Has('Type', 'logical_router')")
        return LRData(data)
