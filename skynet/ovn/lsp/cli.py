import click

from skynet.context import SkyNetCtxt
from skynet.ovn.lsp.data import LSPProvider


@click.group(name='lsp')
@click.pass_obj
def lspcli(obj: SkyNetCtxt) -> None:
    """
    Logical Switch Ports commands
    """
    pass


@lspcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt, switch: str) -> None:
    """
    List Logical Switch Ports
    """
    print(
        LSPProvider(obj).list().to_string(
            ["Name", 'PortType', 'Addresses', 'Options']))
