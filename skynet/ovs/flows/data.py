from typing import Dict, List, Any
import pprint

from skynet.common.data import SkyDiveData, Metadata
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
        pp = pprint.PrettyPrinter(compact=False, width=200, sort_dicts=False)
        for uid, flow in self._data.iterrows():
            pp.pprint(flow.to_dict())
            print("-----------")

    def to_ovs(self):
        """ Experimental (not fully implemented) ovs flow format. It tires to mimic the output of
        ovs-ofproto dump-flows
        """
        fp = OVSFlowPrinter()
        for uid, flow in self._data.iterrows():
            fp.fprint(flow)


class OFFlowProvider:
    def __init__(self, ctxt: SkyNetCtxt):
        self._ctxt = ctxt

    def get(self) -> OFFLowData:
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''
        data = self._ctxt.rest_cli().lookup(
            "g.{at}V().Has('Type', 'ofrule')".format(at=at))

        return OFFLowData(data)
