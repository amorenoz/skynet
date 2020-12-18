import textwrap
import pprint
from pandas import Series


class SeriesPrinter():
    """
    Prints a pandas.Series
    """
    INDENT_STR = " "

    def __init__(self):
        pass

    def print(self, series: Series, indent: int = 0) -> str:
        """
        Return a string representation of the Series.
        Arg:
            indent: The entire string is indented by this level
        """
        out = ""
        header = "|Name: {n}\n|Type: {t}\n|ID: {i}\n".format(
            t=series.get('Type') or "_",
            n=series.get('Name') or "_",
            i=series.name)
        out += header

        tabmin = self._tabmin(series)

        for index in series.index:
            tablen = tabmin - len(index)
            value = pprint.pformat(series.get(index))
            if value.find('\n') > 0:
                format_value = "\n" + textwrap.indent(
                    value, self.INDENT_STR * (len(index) + 4 + tablen))
            else:
                format_value = value
            out += " - {index}:{tab}{value}\n".format(index=index,
                                                      tab=(self.INDENT_STR * tablen),
                                                      value=format_value)

        return textwrap.indent(out, self.INDENT_STR * indent)

    @classmethod
    def _tabmin(cls, series: Series) -> int:
        """
        Minimum tabulation of a series depending on length of indexes
        """
        return len(max(series.index, key=len)) + 4
