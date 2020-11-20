from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider


class LSPData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('UUID'),
        Metadata('OVN.Options', None, 'Options'),
        Metadata('OVN.Addresses', None, 'Addresses'),
        Metadata('OVN.Type', None, 'PortType'),
        Metadata('OVN.ExtID', None, 'ExtID'),
    ]
    """
    LSPData represents Logical Switch Port Data
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        LSPData constructor
        """
        super(LSPData, self).__init__(data=data,
                                      meta=self.METADATA,
                                      index="UUID")


class LSPProvider(SkyDiveDataProvider):
    """
    LSPProvider is a provider for Logical Switches
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LSProvider constructor
        """
        super(LSPProvider, self).__init__(ctxt=ctxt)

    def list(self, switch: str) -> LSPData:
        """
        List the Logical Switch Ports from a given switch
        Args:
            switch: (optional) specify a switch
        """
        query = "V()"

        if switch:
            query += ".Has('Type', 'logical_switch').HasEither('UUID', '{switch}', 'Name', '{switch}').Out()".format(
                switch=switch)

        query += ".Has('Type', 'logical_switch_port')"
        data = self._run_query(query)
        return LSPData(data)
