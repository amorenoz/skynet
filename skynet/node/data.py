from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata


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


class NodeProvider():
    """
    NodeProvider is a provider for K8s Nodes
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LSProvider constructor
        """
        self._ctxt = ctxt

    def get(self) -> NodeData:
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''
        data = self._ctxt.rest_cli().lookup(
            "g.{at}V().Has('Type', 'node')".format(at=at))
        return NodeData(data)
