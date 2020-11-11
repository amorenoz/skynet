import click

from skynet.context import SkyNetCtxt
from skynet.ovn.datapath.data import DatapathProvider


@click.group(name='datapath')
@click.pass_obj
def datapathcli(obj: SkyNetCtxt) -> None:
    """
    Datapath Binding commands
    """
    pass


@datapathcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List Datapath Bindings
    """
    print(DatapathProvider(obj).get().to_string([ 'TunnelKey', 'ExtID']))
