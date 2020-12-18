import click

from skynet.context import SkyNetCtxt
from skynet.host.data import HostDataProvider


@click.group(name='host')
@click.pass_obj
def hostcli(obj: SkyNetCtxt) -> None:
    """
    Host commands
    """


@hostcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List the hosts
    """
    print(
        HostDataProvider(obj).list().to_string(
            columns=['Hostname', 'Platform']))
