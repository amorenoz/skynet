from typing import Dict, List, Any

from skynet.common.data import SkyDiveData, Metadata

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

