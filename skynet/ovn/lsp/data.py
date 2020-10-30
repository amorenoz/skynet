from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata


class LSPData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('UUID'),
        Metadata('OVN.Options', None, 'Options'),
        Metadata('OVN.Addresses', None, 'Addresses'),
        Metadata('OVN.Type', None, 'PortType'),
        #Metadata('OVN.ExtID', None, 'ExtID'),
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


class LSPProvider():
    """
    LSPProvider is a provider for Logical Switches
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LSProvider constructor
        """
        self._ctxt = ctxt

    def get(self) -> LSPData:
        data = self._ctxt.rest_cli().lookup(
            "g.V().Has('Type', 'logical_switch_port')")
        return LSPData(data)
