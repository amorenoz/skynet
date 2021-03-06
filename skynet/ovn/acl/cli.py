import click

from skynet.context import SkyNetCtxt
from skynet.ovn.acl.data import ACLProvider


@click.group(name='acl')
@click.pass_obj
def aclcli(obj: SkyNetCtxt) -> None:
    """
    ACLs commands
    """


@aclcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List ACLs
    """
    print(
        ACLProvider(obj).list().to_string(
            ["Name", 'Host', 'Match', 'Direction', 'Action']))
