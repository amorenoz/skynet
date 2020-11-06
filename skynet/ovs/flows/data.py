from typing import Dict, List, Any
import pprint

from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider
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


class OFFlowProvider(SkyDiveDataProvider):
    """
    OFFlowProvider is a provider for OpenFlowFlows
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LSProvider constructor
        """
        super(OFFlowProvider, self).__init__(ctxt=ctxt)

    def get(self, filter_dict: Dict[str, Any] = {}) -> OFFLowData:
        gremlin_filter = self._gen_gremlin_filter(filter_dict)
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''

        query = "g.{at}V().{filt}".format(at=at, filt=gremlin_filter)
        data = self._ctxt.rest_cli().lookup(query)

        return OFFLowData(data)

    def _gen_gremlin_filter(self, filter_dict: Dict[str, Any]) -> str:
        gremlin_str = "Has('Type', 'ofrule'"
        gremlin_filter = ""
        for filter_key, filter_val in filter_dict.items():
            if isinstance(filter_val, str):
                filter_val_str = "'{}'".format(filter_val)
            elif isinstance(filter_val, int):
                filter_val_str = "{}".format(filter_val)

            gremlin_filter += ",'{}',{}".format(filter_key, filter_val_str)

        return "Has('Type', 'ofrule'{})".format(gremlin_filter)
