from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider, SkyDiveFilter, SkyDiveDataFilter


class LFlowData(SkyDiveData):
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('OVN.LFActions', None, 'Actions'),
        Metadata('OVN.LFMatch', None, 'Match'),
        Metadata('OVN.LFPriority', None, 'Priority'),
        Metadata('OVN.Pipeline', None, 'Pipeline'),
        Metadata('OVN.Table', None, 'Table'),
        Metadata('OVN.ExtID.stage-name', None, 'Stage'),
        Metadata('OVN.ExtID.source', None, 'Source'),
        Metadata('OVN.LogicalDataPath', lambda x: x[0:8]
                 if x and len(x) > 0 else None, 'Datapath'),
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
        if not self.is_empty():
            self._data.sort_values(
                by=['Datapath', 'Pipeline', 'Table', 'Priority'],
                ascending=[True, True, True, False],
                inplace=True)


class LFlowFilter(SkyDiveDataFilter):
    """
    Logical Flow filters
    """
    def __init__(self):
        filters = [
            SkyDiveFilter("Table", int, "OVN.Table"),
            SkyDiveFilter("Pipeline", SkyDiveFilter.string, "OVN.Pipeline"),
            SkyDiveFilter("Datapath", lambda x: "Regex('{}.*')".format(x),
                          "OVN.LogicalDataPath"),
            SkyDiveFilter("Match", SkyDiveFilter.regex, "OVN.LFMatch"),
            SkyDiveFilter("Actions", SkyDiveFilter.regex, "OVN.LFActions")
        ]
        super(LFlowFilter, self).__init__(filters)


class LFlowProvider(SkyDiveDataProvider):
    """
    LFlowProvider is a provider for Logical Flows
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        LFlowProvider constructor
        """
        super(LFlowProvider, self).__init__(ctxt=ctxt)

    def list(self, filter_obj: LFlowFilter = None) -> LFlowData:
        gremlin_filter = filter_obj.generate_gremlin() if filter_obj else ""
        query = "V().Has('Type', 'logical_flow'){filt}".format(
            filt=gremlin_filter)
        data = self._run_query(query)
        return LFlowData(data)
