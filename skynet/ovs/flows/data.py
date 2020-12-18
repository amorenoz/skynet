from typing import Dict, List, Any
from functools import partial
import pprint

from skynet.common.data import SkyDiveData, Metadata, Field, \
    SkyDiveDataProvider, SkyDiveFilter, SkyDiveDataFilter, \
    SkyDivePostFilter
from skynet.context import SkyNetCtxt
from skynet.ovs.flows.ovs_printer import OVSFlowPrinter


class OFFLowData(SkyDiveData):
    METADATA: List[Field] = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('Cookie'),
        Metadata('Actions'),
        Metadata('Metric'),
        Metadata('Filters'),
        Metadata('Table'),
        Metadata('Priority'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        super(OFFLowData, self).__init__(data=data,
                                         meta=self.METADATA,
                                         index="ID")
        if not self.is_empty():
            self._data.sort_values(by=['Table', 'Priority'],
                                   ascending=[True, False],
                                   inplace=True)

    def to_text(self):
        """
        Pretty print each flow
        """
        if self.is_empty():
            return "No data"

        pp = pprint.PrettyPrinter(compact=False, width=200, sort_dicts=False)
        for uid, flow in self._data.iterrows():
            pp.pprint(flow.to_dict())
            print("-----------")

    def to_ovs(self):
        """ Experimental (not fully implemented) ovs flow format. It tires to mimic the output of
        ovs-ofproto dump-flows
        """
        if self.is_empty():
            return "No data"

        fp = OVSFlowPrinter()
        for uid, flow in self._data.iterrows():
            fp.fprint(flow)


class OFFlowFilter(SkyDiveDataFilter):
    """
    OFFLow-specific filters
    """
    def __init__(self):
        filters = [
            SkyDiveFilter("Table", int),
            SkyDiveFilter("Cookie", self.cookie),
            SkyDiveFilter("Priority", int),
            SkyDiveFilter("Host", SkyDiveFilter.string)
        ]
        post_filters = [
            SkyDivePostFilter('eth_src', partial(self.field_match, 'eth_src'),
                              None),
            SkyDivePostFilter('eth_dst', partial(self.field_match, 'eth_dst'),
                              None),
            SkyDivePostFilter('ipv4_dst', partial(self.field_match,
                                                  'ipv4_dst'), None),
            SkyDivePostFilter('ipv4_src', partial(self.field_match,
                                                  'ipv4_src'), None),
            SkyDivePostFilter('eth_type', partial(self.field_match,
                                                  'eth_type'), None),
            SkyDivePostFilter('tcp_dst', partial(self.field_match, 'tcp_dst'),
                              int),
            SkyDivePostFilter('tcp_src', partial(self.field_match, 'tcp_src'),
                              int),
            SkyDivePostFilter('ip_proto', partial(self.field_match,
                                                  'ip_proto'), None),
            SkyDivePostFilter('eth_type', partial(self.field_match,
                                                  'eth_type'), None),
            SkyDivePostFilter('in_port', partial(self.field_match, 'in_port'),
                              int),
        ]

        super(OFFlowFilter, self).__init__(filters, post_filters)

    @classmethod
    def cookie(cls, cookie: str) -> int:
        return int(cookie, 16)

    @classmethod
    def field_match(cls, field_type: str, item: Dict, value: Any) -> bool:
        return {
            "Type": field_type,
            "Value": value
        } in item['Metadata']['Filters']


class OFFlowProvider(SkyDiveDataProvider):
    """
    OFFlowProvider is a provider for OpenFlowFlows
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        OFFlowProvider constructor
        """
        super(OFFlowProvider, self).__init__(ctxt=ctxt)

    def list(self,
             host: str = "",
             bridge: str = "",
             filter_obj: OFFlowFilter = None) -> OFFLowData:
        """
        Get the Openflow Flows based on a filter
        """
        query = "V()"
        gremlin_filter = filter_obj.generate_gremlin() if filter_obj else ""

        if host:
            query += ".Has('Type', 'host').HasEither('ID', '{host}', 'Name', '{host}').Out()".format(
                host=host)

        if bridge:
            query += ".Has('Type', 'ovsbridge').HasEither('ID', '{bridge}', 'Name', '{bridge}').Out()".format(
                bridge=bridge)
        elif host:
            query += ".Out()"

        query += ".Has('Type', 'ofrule'){filt}".format(filt=gremlin_filter)

        data = self._run_query(query)
        processed_data = filter_obj.post_process(data) if filter_obj else data

        return OFFLowData(processed_data)
