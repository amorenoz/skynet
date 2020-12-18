from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Field, Metadata, \
    SkyDiveDataProvider


class ACLData(SkyDiveData):
    METADATA: List[Field] = [
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


class ACLProvider(SkyDiveDataProvider):
    """
    ACLProvider is a provider for ACLs
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        ACLProvider constructor
        """
        super(ACLProvider, self).__init__(ctxt=ctxt)

    def list(self) -> ACLData:
        query = "V().Has('Type', 'acl')"
        data = self._run_query(query)

        return ACLData(data)
