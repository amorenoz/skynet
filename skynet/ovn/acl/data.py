from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata


class ACLData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('OVN.Action', None, 'Action'),
        Metadata('OVN.Match', None, 'Match'),
        Metadata('OVN.Direction', None, 'Direction'),
    ]
    """
    ACLData represents Logical Router Data
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        ACLData constructor
        """
        super(ACLData, self).__init__(data=data,
                                      meta=self.METADATA,
                                      index="ID")


class ACLProvider():
    """
    ACLProvider is a provider for ACLs
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        ACLProvider constructor
        """
        self._ctxt = ctxt

    def get(self) -> ACLData:
        data = self._ctxt.rest_cli().lookup("g.V().Has('Type', 'acl')")
        return ACLData(data)
