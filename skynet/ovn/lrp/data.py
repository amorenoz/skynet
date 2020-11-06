from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider


class LRPData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('UUID'),
        Metadata('Enabled'),
        Metadata('MAC'),
        Metadata('OVN.Networks', None, 'Networks'),
    ]
    """
    LRPData represents Logical Router Data
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        LRPData constructor
        """
        super(LRPData, self).__init__(data=data,
                                      meta=self.METADATA,
                                      index="UUID")


class LRPProvider(SkyDiveDataProvider):
    """
    LRPProvider is a provider for Logical Router Ports
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LRPProvider constructor
        """
        super(LRPProvider, self).__init__(ctxt=ctxt)

    def get(self) -> LRPData:
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''

        query = "g.{at}V().Has('Type', 'logical_router_port')".format(at=at)
        data = self._run_query(query)
        return LRPData(data)
