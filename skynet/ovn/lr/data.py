from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider


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


class LRProvider(SkyDiveDataProvider):
    """
    LRProvider is a provider for Logical Routers
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LRProvider constructor
        """
        super(LRProvider, self).__init__(ctxt=ctxt)

    def get(self) -> LRData:
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''

        query = "g.{at}V().Has('Type', 'logical_router')".format(at=at)
        data = self._run_query(query)
        return LRData(data)
