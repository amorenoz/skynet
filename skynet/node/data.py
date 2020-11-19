from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider


class NodeData(SkyDiveData):
    """
    NodeData represents Logical Switch Data
    """
    METADATA = [
        Metadata('UUID'),
        Metadata('Type'),
        Metadata('K8s.Extra.ObjectMeta.Annotations.k8s.ovn'),
        Metadata('ClusterName'),
        Metadata('K8s.Kernel', None, 'Kernel'),
        Metadata('K8s.InternalIP', None, 'InternalIP'),
        Metadata('K8s.Hostname', None, 'Hostname'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        NodeData constructor
        """
        super(NodeData, self).__init__(data=data,
                                       meta=self.METADATA,
                                       index="ID")


class NodeProvider(SkyDiveDataProvider):
    """
    NodeProvider is a provider for K8s Nodes
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        NodeProvider constructor
        """
        super(NodeProvider, self).__init__(ctxt=ctxt)

    def list(self) -> NodeData:
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''

        query = "g.{at}V().Has('Type', 'node')".format(at=at)

        data = self._run_query(query)
        return NodeData(data)
