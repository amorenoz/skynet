from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveDataProvider
from skynet.ovn.lsp.model import LSPData
from skynet.ovn.ls.data import LSData
from skynet.ovn.lrp.data import LRPData
from skynet.k8s.data import PodData
from skynet.ovs.bridge.data  import OvSIfaceData

class LogicalSwitchPort():
    """
    LogicalSwitchPort encapsulates the detail information of a Logical Switch Port
    It has three properties:
        lsp: The lsp information (LSPData)
        ls: The logical switch (LSData)
        lsp: The logical router port to which is connected
        pod: The pod to whitch it's connected
        iface : The interface to whitch it's connected
    """
    def __init__(self, lsp_data: List[Dict[str, Any]], both_data: List[Dict[str, Any]]):
        """
        Create  LogicalSwitchPort from skydive data
        lsp_data is the LSP raw data
        both_data is the output of query "g.V({}).Both()"
        """
        self._lsp = LSPData(lsp_data)
        self._ls = LSData(list(
            filter(lambda d: d['Metadata']['Type'] == 'logical_switch',
                   both_data)))
        self._lrp = LRPData(list(
            filter(lambda d: d['Metadata']['Type'] == 'logical_router_port',
                   both_data)))
        self._pod= PodData(list(
            filter(lambda d: d['Metadata']['Type'] == 'pod',
                   both_data)))
        self._iface = OvSIfaceData(list(
            filter(lambda d: d['Metadata']['Type'] == 'veth',
                   both_data)))

    @property
    def lsp(self) -> LSPData:
        return self._lsp
    @property
    def ls(self) -> LSData:
        return self._ls
    @property
    def lrp(self) -> LRPData:
        return self._lrp
    @property
    def pod(self) -> PodData:
        return self._pod
    @property
    def iface(self) -> OvSIfaceData:
        return self._iface


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

    def get(self, lsp: str) -> LogicalSwitchPort:
        """
        Get a Logical Switch Port from uuid
        """
        query = "V().Has('Type', 'logical_switch_port', 'UUID', '{lsp}')".format(lsp=lsp)
        lsp_data = self._run_query(query)

        if len(lsp_data) == 0:
            raise Exception('Logical Switch Port not found')

        query += ".Both()"
        both_data = self._run_query(query)

        return LogicalSwitchPort(lsp_data, both_data)


