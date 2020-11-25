from typing import Optional, Dict, Any, List

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveDataProvider, SkyDiveData, Metadata, SkyDiveFilter, SkyDiveDataFilter


class PodData(SkyDiveData):
    """
    Pod Data from Skydive
    """
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('K8s.Namespace', None, 'Namespace'),
        Metadata('K8s.Status', None, 'Status'),
        Metadata('K8s.IP', None, 'IP'),
        Metadata('K8s.Node', None, 'Node'),
        Metadata('K8s.Extra.HostNetwork', None, 'HostNetwork'),
        Metadata('K8s.Extra.Status.HostIP', None, 'HostIP'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        super(PodData, self).__init__(data=data,
                                      meta=self.METADATA,
                                      index="ID")


class ContainerData(SkyDiveData):
    """
    Container Data from Skydive
    """
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('K8s.Namespace', None, 'Namespace'),
        Metadata('K8s.Pod', None, 'Pod'),
        Metadata('K8s.Extra.Ports', None, 'Ports'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        super(ContainerData, self).__init__(data=data,
                                            meta=self.METADATA,
                                            index="ID")


class K8sFilter(SkyDiveDataFilter):
    """
    K8s filters
    """
    def __init__(self):
        filters = [
            SkyDiveFilter('Namespace', SkyDiveFilter.string, 'K8s.Namespace'),
            SkyDiveFilter('Pod', SkyDiveFilter.string, 'K8s.Pod'),
        ]
        super(K8sFilter, self).__init__(filters)


class K8sProvider(SkyDiveDataProvider):
    """
    Data Provider for K8s
    """
    def __init__(self, ctxt: SkyNetCtxt):
        super(K8sProvider, self).__init__(ctxt=ctxt)

    def list_pods(self, filter_obj: K8sFilter) -> PodData:
        """
        List Pods
        """
        gremlin_filter = filter_obj.generate_gremlin() if filter_obj else ""

        query = "V().Has('Manager', 'k8s', 'Type', 'pod'){filt}".format(
            filt=gremlin_filter)
        data = self._run_query(query)
        return PodData(data)

    def list_containers(self, filter_obj: K8sFilter) -> ContainerData:
        """
        List Containers
        """
        gremlin_filter = filter_obj.generate_gremlin() if filter_obj else ""

        query = "V().Has('Manager', 'k8s', 'Type', 'container'){filt}".format(
            filt=gremlin_filter)
        data = self._run_query(query)
        return ContainerData(data)
