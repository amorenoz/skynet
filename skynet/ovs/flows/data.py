from typing import Dict, List, Any
import pprint

from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider, SkyDiveFilter, SkyDiveDataFilter
from skynet.context import SkyNetCtxt
from skynet.ovs.flows.ovs_printer import OVSFlowPrinter


class OFFLowData(SkyDiveData):
    METADATA = [
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
            SkyDiveFilter("Cookie", SkyDiveFilter.string),
            SkyDiveFilter("Priority", int),
            SkyDiveFilter("Host", SkyDiveFilter.string)
        ]
        super(OFFlowFilter, self).__init__(filters)


class OFFlowProvider(SkyDiveDataProvider):
    """
    OFFlowProvider is a provider for OpenFlowFlows
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        OFFlowProvider constructor
        """
        super(OFFlowProvider, self).__init__(ctxt=ctxt)

    def list(self, filter_obj: OFFlowFilter = None) -> OFFLowData:
        """
        Get the Openflow Flows based on a filter
        """
        gremlin_filter = filter_obj.generate_gremlin() if filter_obj else ""
        query = "V().Has('Type', 'ofrule'){filt}".format(filt=gremlin_filter)

        data = self._run_query(query)

        return OFFLowData(data)
