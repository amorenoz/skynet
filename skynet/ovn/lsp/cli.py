import click

from skynet.context import SkyNetCtxt
from skynet.ovn.lsp.data import LSPProvider


@click.group(name='lsp')
@click.pass_obj
def lspcli(obj: SkyNetCtxt) -> None:
    """
    Logical Switch Pororts commands
    """
    pass


@lspcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List Logical Switch Ports
    """
    print(
        LSPProvider(obj).get().to_string(
            ["Name", 'PortType', 'Addresses', 'Options']))
