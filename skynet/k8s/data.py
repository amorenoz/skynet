from typing import Optional, Dict, Any, List

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveDataProvider, SkyDiveData, Metadata, SkyDiveFilter, SkyDiveDataFilter
from skynet.ovn.lsp.data import LSPData
from skynet.ovs.bridge.data import OvSIfaceData


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


class Pod():
    """
    Pod encapsulates the detail information of a Pod from a skydive query
    It has three properties:
        pod: The pod information (PodData)
        containers: The pod information (ContainerData)
        lsp: The logical switch port connected to the pod LSPData
        netns: The network namespace of the pod
        iface: The OvS Interface connected to the pod
    """
    def __init__(self, pod_data: List[Dict[str, Any]],
                 container_data: List[Dict[str, Any]],
                 lsp_data: List[Dict[str, Any]], veth_data: List[Dict[str,
                                                                      Any]]):
        """
        """
        self._pod = PodData(pod_data)

        self._containers = ContainerData(container_data)

        self._lsp = LSPData(lsp_data)

        self._iface = OvSIfaceData(veth_data)

    @property
    def pod(self) -> PodData:
        return self._pod

    @property
    def lsp(self) -> LSPData:
        return self._lsp

    @property
    def iface(self) -> OvSIfaceData:
        return self._iface

    @property
    def containers(self) -> ContainerData:
        return self._containers


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

    def get_pod(self, pod: str) -> Pod:
        """
        Get Pod details
        """
        query = "V().Has('Manager', 'k8s', 'Type', 'pod', 'ID', '{pod}')".format(
            pod=pod)

        pod_data = self._run_query(query)

        if len(pod_data) == 0:
            raise Exception('Pod not found')

        query += ".Out()"
        pod_out_data = self._run_query(query)

        container_data = list(
            filter(lambda d: d['Metadata']['Type'] == 'container',
                   pod_out_data))

        lsp_data = list(
            filter(lambda d: d['Metadata']['Type'] == 'logical_switch_port',
                   pod_out_data))

        if len(lsp_data) > 0:
            lsp_name = lsp_data[0]['Metadata']['Name']

            veth_query = "V().Has('Type', 'veth', 'ExtID.iface-id', '{iface_id}')".format(
                iface_id=lsp_name)

            veth_data = self._run_query(veth_query)


        return Pod(pod_data, container_data, lsp_data, veth_data)
