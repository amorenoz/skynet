from typing import Dict, List, Any

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

    def list(self, router: str) -> LRPData:
        """
        List the Logical Router Ports from a given router
        Args:
            switch: (optional) specify a switch
        """
        query = "V()"

        if router:
            query += ".Has('Type', 'logical_router').HasEither('UUID', '{router}', 'Name', '{router}').Out()".format(
                router=router)

        query += ".Has('Type', 'logical_router_port')"
        data = self._run_query(query)
        return LRPData(data)
