import logging
from typing import Dict, List, Callable, Any, Optional
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
                logging.getLogger("Data").debug("key {} not found in dictionary {}".format(
                    self.name, data))
                continue

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
        Args:
            query: The query string
                It must not contain the initial G.At() , that part will be prepended by
                this function
        """

        at = "At('%s')." % self._ctxt.options().get(
            'at') if self._ctxt.options().get('at') else ''

        full_query = "G.{at}{query}".format(at=at, query=query)

        log = logging.getLogger("Data")
        log.debug('Query: %s' % full_query)
        data = self._ctxt.rest_cli().lookup(full_query)
        log.debug('Result len: %i' % len(data))

        return data


class SkyDiveFilterError(Exception):
    pass


class SkyDiveFilter:
    """
    SkyDiveFilter defines one filter information
    Instances of SkyDiveFilters can be created to define filters. A filter is composed of:
        - a name which will be used for parsing the filter string
        - a key_name which is the key that will be used for actual filtering in SkyDive
        - a transformation function that massages the value of the filter to accomodate it to the SkyDive Filter
            This class includes some predefined transformation functions
    """
    def __init__(self, name: str, trans: Any = None, key_name: str = ""):
        """
        SkyDiveFilter contructor
        Args:
            name: The name of the filter as specified by the user
            trans: (optional) The name transformation to apply to the filter data before adding it to the gremlin filter
            key_name: (optional) The key name to apply the filter to (default: same mas 'name')
        """
        self.name = name
        self.trans = trans if trans else self.noop
        self.key_name = key_name if key_name != "" else name

    @classmethod
    def noop(cls, val):
        """
        Simplest of transformation functions
        """
        return val

    @classmethod
    def string(cls, val):
        """
        Simple tranformation function that just single-quotes the string
        """
        return "'{}'".format(val)


class SkyDiveDataFilter:
    """
    SkyDiveFilter implements filtering on skydive queries
    """
    def __init__(self, filters: List[SkyDiveFilter]):
        """
        SkyDiveDataFilter constructor from a list of SkyDiveFilters
        """
        self._filters = filters

    def _filter_names(self) -> List[str]:
        return [f.name for f in self._filters]

    def _get_filter(self, name) -> SkyDiveFilter:
        for f in self._filters:
            if f.name == name:
                return f
        raise SkyDiveFilterError('Filter not found: %s' % name)

    def process_string(self, filter_str: str) -> None:
        """
        Run the filter The Filter Format is as follows:
        Key1=Val1,Key2=Val2
        The Conditions are ANDed

        raises: SkyDiveFilterError if there is an
        issue with the string format
        """
        self._processed = {}
        if filter_str == "":
            return

        for filter_elem in filter_str.split(','):
            filter_parts = filter_elem.split('=')
            if len(filter_parts) != 2:
                raise SkyDiveFilterError('Wrong filter format')
            key = filter_parts[0]
            val = filter_parts[1]
            if not key or not val:
                raise SkyDiveFilterError('Wrong filter format')
            filter_obj = self._get_filter(key)

            self._processed[filter_obj.key_name] = filter_obj.trans(val)

    def generate_gremlin(self) -> str:
        """
        Generate a gremlin query string based on a the filter
        """
        gremlin_filters = []
        if not self._processed:
            return ""

        for filter_key, filter_val in self._processed.items():
            filter_val_str = "{}".format(filter_val)
            gremlin_filters.append("'{}',{}".format(filter_key,
                                                    filter_val_str))

        return '.Has({})'.format(
            ','.join(gremlin_filters) if len(gremlin_filters) > 0 else "")
