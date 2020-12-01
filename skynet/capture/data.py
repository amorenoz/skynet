from typing import Dict, Any, List
from skydive.captures import Capture
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Field, SkyDiveDataProvider


class CaptureData(SkyDiveData):
    """
    CaptureData represets a capture in Skydive's Database
    """
    BASIC_FIELDS = {}
    METADATA = [
        Field('UUID'),
        Field('GremlinQuery'),
        Field('LayeredKeyMode'),
        Field('Count'),
        Field('PollingInterval'),
        Field('Name'),
        Field('Description'),
    ]

    def __init__(self, cap_data: List[Capture]):
        super(CaptureData,
              self).__init__(data=[cap.repr_json() for cap in cap_data],
                             meta=self.METADATA,
                             index="UUID")


class FlowData(SkyDiveData):
    """
    Flow Data represents a Flow list in skydive database
    """
    BASIC_FIELDS = {}
    METADATA = [
        Field('UUID'),
        Field('LayersPath'),
        Field('Application'),
        Field('Link.Protocol', None, 'LinkProtocol'),
        Field('Link.A', None, 'LinkSrc'),
        Field('Link.B', None, 'LinkDst'),
        Field('Network.Protocol', None, 'NetworkProtocol'),
        Field('Network.A', None, 'NetworkSrc'),
        Field('Network.B', None, 'NetworkDst'),
        Field('Transport.Protocol', None, 'TransportProtocol'),
        Field('Transport.A', None, 'TransportSrc'),
        Field('Transport.B', None, 'TransportDst'),
        Field('Metric.ABPackets', None, 'Packets'),
        Field('Metric.ABBytes', None, 'Bytes'),
        Field('Metric.BAPackets', None, 'ReturnPackets'),
        Field('Metric.BABytes', None, 'ReturnBytes'),
        Field('Start', None, 'Start'),
        Field('Last', None, 'Last'),
        Field('TrackingID', None, 'TrackingID'),
        Field('L3TrackingID', None, 'L3TrackingID'),
        Field('NodeTID', None, 'NodeTID'),
        Field('CaptureID', None, 'CaptureID'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        """
        super(FlowData, self).__init__(data=data,
                                       meta=self.METADATA,
                                       index="UUID")


class CaptureProvider(SkyDiveDataProvider):
    """
    Backend provider for Captures
    """
    def __init__(self, ctxt: SkyNetCtxt):
        super(CaptureProvider, self).__init__(ctxt=ctxt)

    def list(self) -> CaptureData:
        """
        List active captures
        """
        captures = []
        cap_data = self._ctxt.rest_cli().capture_list()
        return CaptureData(cap_data)

    def create(self, bpf: str, name: str, description: str,
               interface: str) -> CaptureData:
        """
        Create a capture
        """
        gremlin = "G.V().Has('Name', '{}')".format(interface)
        cap_data = self._ctxt.rest_cli().capture_create(
            query=gremlin, name=name, description=description, bpf_filter=bpf)

        return CaptureData([cap_data])

    def get(self, capture: str) -> FlowData:
        """
        Get a Capture (it's flows)
        """
        query = "Flows().Has('CaptureID', '{}')".format(capture)
        data = self._run_query(query)
        return FlowData(data)

    def delete(self, capture: str) -> None:
        """
        Get a Capture (it's flows)
        """
        self._ctxt.rest_cli().capture_delete(capture)
