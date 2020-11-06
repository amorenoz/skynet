import logging
from typing import Dict, List, Callable, Any
from pandas import DataFrame, Timestamp

from skynet.context import SkyNetCtxt

MetadataList = List[Dict[str, Callable]]
RawData = List[Dict[str, Any]]


class Metadata:
    """
    A Metadata field defines a metadata field that needs to be extracted from the Skydive data
    It has the following values
    name: The name of the Field. Nested fields can be accessed with ".", eg: "L0.L1"
    trans: The transformation callable to apply to the value if any
    key_name: The name of the key in the resulting field
    """
    def __init__(self,
                 name: str,
                 trans: Callable = None,
                 key_name: str = None):
        self.name = name
        self.key_name = key_name if key_name else name
        self.trans = trans

    def value(self, data: Dict[str, Any]) -> Any:
        """
        Extract the Metadata Value from the given data dictionary
        """
        value = data.get('Metadata')
        for key in self.name.split('.'):
            if not value:
                raise Exception("key {} not found in dictionary {}".format(
                    self.name, data))
            value = value.get(key)

        return self.trans(value) if self.trans else value

    def key(self):
        return self.key_name


class SkyDiveData:
    """
    SkyDiveData defines a base class for data encapsulations coming from Skydive
    It provides basic data manipulation functionality
    """
    BASIC_FIELDS = {
        "ID": None,
        "Host": None,
        "CreatedAt": Timestamp,
        "UpdatedAt": Timestamp,
        "DeletedAt": Timestamp,
    }

    def __init__(self,
                 data: RawData,
                 meta: List[Metadata],
                 index: str = None) -> None:
        """
        SkyDiveData Constructor
        Args:
            data: The raw data coming from SkyDive
            meta: The list of Metadata fields to process
            index: The key that shall be used as index
        """
        self._raw = data
        self._index = index
        self._meta = meta
        self._data = self._to_dataframe()

    def is_empty(self):
        """
        Returns whether the data is empty
        """
        return len(self._raw) == 0

    def to_string(self,
                  columns: List[str] = None,
                  justify: str = "center") -> str:
        """
        Print the data into a string
        """
        if self.is_empty():
            return "No data"

        return self._data.to_string(columns=columns, justify=justify)

    def to_json(self, *args, **kwargs):
        """
        Print to json. Based on Dataframe.to_json. See:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
        """
        if self.is_empty():
            return "{}"
        return self._data.to_json(*args, **kwargs)

    def to_html(self, *args, **kwargs):
        """
        Print to html. Based on Dataframe.to_html. See:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html
        """
        if self.is_empty():
            return "No data"

        return self._data.to_html(*args, **kwargs)

    def data(self) -> DataFrame:
        """
        Returns the processed DataFrame
        """
        return self._data

    def _to_dataframe(self) -> DataFrame:
        """
        Process the raw data into a DataFrame
        """
        if len(self._raw) == 0:
            return None

        dataframe = DataFrame.from_records(data=self._extract(),
                                           index=self._index)
        return dataframe

    def _extract(self) -> List[Dict[str, Any]]:
        """"
        Extract the relevant metadata from the raw data
        """
        extracted = [{
            **{
                field: trans(el[field]) if trans else el[field]
                for field, trans in self.BASIC_FIELDS.items()
            },
            **{meta.key(): meta.value(el)
               for meta in self._meta}
        } for el in self._raw]
        return extracted


class SkyDiveDataProvider:
    """
    SkyDiveDataProvider serves as base class for other providers
    giving some basic common functionality
    """
    def __init__(self, ctxt: SkyNetCtxt) -> None:
        """
        Constructor
        """
        self._ctxt = ctxt

    def _run_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Run a Skydive Query
        """
        log = logging.getLogger("Data")
        log.debug('Query: %s' % query)
        data = self._ctxt.rest_cli().lookup(query)
        log.debug('Result len: %i' % len(data))

        return data

    @classmethod
    def _gen_gremlin_filter(cls, filter_dict: Dict[str, Any]) -> str:
        """
        Generate a gremlin query string based on a dictionary of filters
        """
        gremlin_filter = ""
        for filter_key, filter_val in filter_dict.items():
            if isinstance(filter_val, str):
                filter_val_str = "'{}'".format(filter_val)
            elif isinstance(filter_val, int):
                filter_val_str = "{}".format(filter_val)

            gremlin_filter += "'{}',{}".format(filter_key, filter_val_str)

        return '.Has({})'.format(
            gremlin_filter) if len(gremlin_filter) > 0 else ""

