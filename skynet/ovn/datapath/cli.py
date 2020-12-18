import click

from skynet.context import SkyNetCtxt
from skynet.ovn.datapath.data import DatapathProvider, DatapathFilter


@click.group(name='datapath')
@click.pass_obj
def datapathcli(obj: SkyNetCtxt) -> None:
    """
    Datapath Binding commands
    """


@datapathcli.command()
@click.argument('filter', required=False, default="")
@click.pass_obj
def list(obj: SkyNetCtxt, filter: str) -> None:
    """
    List Datapath Bindings

    \b
    FILTER is a Filter string formatted as "Filter1=Value1,Filter2=Value2,..."
    Supported Filters:
        TunnelKey   [TunnelKey] (tunnel key integer)
        Router      [UUID] (uuid of the logical router)
        Switch      [UUID] (uuid of the logical switch)
    E.g: TunnelKey=3,Router=9bcee0e7-b24a-4727-a5ee-5eb797e3dd2a
    """
    filter_obj = DatapathFilter()
    filter_obj.process_string(filter)
    print(
        DatapathProvider(obj).list(filter_obj).to_string(
            ['TunnelKey', 'ExtID']))
