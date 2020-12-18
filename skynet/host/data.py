from typing import Dict, Any, List

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveDataProvider, SkyDiveData, Metadata


class HostData(SkyDiveData):
    """
    HostData represents a Host data in Skydive
    """
    METADATA = [
        Metadata('Type'),
        Metadata('Hostname'),
        Metadata('VirtualizationSystem'),
        Metadata('VirtualizationRole'),
        Metadata('OS'),
        Metadata('PlatformFamily'),
        Metadata('Platform'),
        Metadata('PlatformVersion'),
        Metadata('KernelCmdLine'),
        Metadata('KernelVersion'),
        Metadata('CPU'),
        Metadata('Sockets'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        HostData Constructor
        """
        super(HostData, self).__init__(data=data,
                                       meta=self.METADATA,
                                       index="ID")


class HostDataProvider(SkyDiveDataProvider):
    """
    Data Provider for Hosts
    """
    def __init__(self, ctxt: SkyNetCtxt):
        super(HostDataProvider, self).__init__(ctxt=ctxt)

    def list(self) -> HostData:
        """
        List Hosts
        """
        query = "V().Has('Type', 'host')"

        data = self._run_query(query)
        return HostData(data)
