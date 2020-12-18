import click

from skynet.context import SkyNetCtxt
from skynet.ovn.lr.data import LRProvider


@click.group(name='lr')
@click.pass_obj
def lrcli(obj: SkyNetCtxt) -> None:
    """
    Logical Router commands
    """


@lrcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List Logical Routers
    """
    print(LRProvider(obj).list().to_string(["Name", 'Host', 'ExtID']))
