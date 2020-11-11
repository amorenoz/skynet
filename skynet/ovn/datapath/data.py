from typing import Dict, List, Any
from pandas import DataFrame

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveData, Metadata, SkyDiveDataProvider


class DatapathData(SkyDiveData):
    METADATA = [
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


class DatapathProvider(SkyDiveDataProvider):
    """
    DatapathProvider is a provider for Datapath Bindings
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        DatapathProvider constructor
        """
        super(DatapathProvider, self).__init__(ctxt=ctxt)

    def get(self) -> DatapathData:
        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''

        query = "g.{at}V().Has('Type', 'datapath_binding')".format(at=at)
        data = self._run_query(query)
        return DatapathData(data)
