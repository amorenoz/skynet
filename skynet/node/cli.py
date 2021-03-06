import click

from skynet.context import SkyNetCtxt
from skynet.node.data import NodeProvider


@click.group(name='node')
@click.pass_obj
def nodecli(obj: SkyNetCtxt) -> None:
    """
    Node commands
    """


@nodecli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List existing nodes
    """
    print(
        NodeProvider(obj).list().to_string(
            ['ClusterName', 'Kernel', 'InternalIP', 'Hostname']))
