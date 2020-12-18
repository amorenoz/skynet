from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Field, Metadata, \
    SkyDiveDataProvider


class LRData(SkyDiveData):
    METADATA: List[Field] = [
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


class LRProvider(SkyDiveDataProvider):
    """
    LRProvider is a provider for Logical Routers
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LRProvider constructor
        """
        super(LRProvider, self).__init__(ctxt=ctxt)

    def list(self) -> LRData:
        query = "V().Has('Type', 'logical_router')"
        data = self._run_query(query)
        return LRData(data)
