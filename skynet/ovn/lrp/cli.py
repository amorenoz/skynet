import click

from skynet.context import SkyNetCtxt
from skynet.ovn.lrp.data import LRPProvider


@click.group(name='lrp')
@click.pass_obj
def lrpcli(obj: SkyNetCtxt) -> None:
    """
    Logical Router Ports commands
    """
    pass


@lrpcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List Logical Router Ports
    """
    print(
        LRPProvider(obj).list().to_string(
            columns=["Name", 'MAC', 'Enabled', 'Networks']))
