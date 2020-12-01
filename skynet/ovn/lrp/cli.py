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
@click.option('-r',
              '--router',
              'router',
              help='Only list the Logical Ports corresponding to '
              'the specified Logical Router'
              '(Either name or UUID are acceptable values)')
@click.pass_obj
def list(obj: SkyNetCtxt, router: str) -> None:
    """
    List Logical Router Ports
    """
    print(
        LRPProvider(obj).list(router).to_string(
            columns=["Name", 'MAC', 'Enabled', 'Networks']))
