from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider


class LFlowData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('OVN.LFActions', None, 'Actions'),
        Metadata('OVN.LFMatch', None, 'Match'),
        Metadata('OVN.LFPriority', None, 'Priority'),
        Metadata('OVN.Pipeline', None, 'Pipeline'),
        Metadata('OVN.Table', None, 'Table'),
        Metadata('OVN.LogicalDataPath', lambda x: x[0:8] if len(x) > 0 else None, 'DataPath'),
    ]
    """
    LFlowData represents Logical Flow Data
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        LFlowData constructor
        """
        super(LFlowData, self).__init__(data=data,
                                     meta=self.METADATA,
                                     index="Name")


class LFlowProvider(SkyDiveDataProvider):
    """
    LFlowProvider is a provider for Logical Flows
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LFlowProvider constructor
        """
        super(LFlowProvider, self).__init__(ctxt=ctxt)

    def get(self) -> LFlowData:
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''

        query = "g.{at}V().Has('Type', 'logical_flow')".format(at=at)
        data = self._run_query(query)
        return LFlowData(data)
