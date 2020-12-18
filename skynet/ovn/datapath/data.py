from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Field, Metadata, \
    SkyDiveDataProvider, SkyDiveFilter, SkyDiveDataFilter


class DatapathData(SkyDiveData):
    METADATA: List[Field] = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('OVN.TunnelKey', None, 'TunnelKey'),
        Metadata('OVN.ExtID', None, 'ExtID'),
    ]
    """
    DatapathData represents Datapath Binding Data
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        DatapathData constructor
        """
        super(DatapathData, self).__init__(data=data,
                                           meta=self.METADATA,
                                           index="Name")


class DatapathFilter(SkyDiveDataFilter):
    """
    DatapathFilter filters
    """
    def __init__(self):
        filters = [
            SkyDiveFilter('TunnelKey', int, 'OVN.TunnelKey'),
            SkyDiveFilter('Switch', SkyDiveFilter.string,
                          'OVN.ExtID.logical-switch'),
            SkyDiveFilter('Router', SkyDiveFilter.string,
                          'OVN.ExtID.logical-router'),
        ]
        super(DatapathFilter, self).__init__(filters)


class DatapathProvider(SkyDiveDataProvider):
    """
    DatapathProvider is a provider for Datapath Bindings
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        DatapathProvider constructor
        """
        super(DatapathProvider, self).__init__(ctxt=ctxt)

    def list(self, filter_obj: DatapathFilter) -> DatapathData:
        gremlin_filter = filter_obj.generate_gremlin() if filter_obj else ""

        query = "V().Has('Type', 'datapath_binding'){filt}".format(
            filt=gremlin_filter)
        data = self._run_query(query)
        return DatapathData(data)
