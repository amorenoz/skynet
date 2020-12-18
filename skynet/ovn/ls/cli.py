import click

from skynet.context import SkyNetCtxt
from skynet.ovn.ls.data import LSProvider


@click.group(name='ls')
@click.pass_obj
def lscli(obj: SkyNetCtxt) -> None:
    """
    Logical Switch commands
    """


@lscli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List Logical Switches
    """
    print(LSProvider(obj).list().to_string(["Name", 'Host', 'ExtID']))
