import click

from skynet.common.printers import SeriesPrinter
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
@click.option('-s',
              '--switch',
              'switch',
              help='Only list the Logical Ports corresponding to '
              'the specified Logical Switch'
              '(Either name or UUID are acceptable values)')
@click.pass_obj
def list(obj: SkyNetCtxt, switch: str) -> None:
    """
    List Logical Switch Ports
    """
    print(
        LSPProvider(obj).list(switch).to_string(
            ["Name", 'PortType', 'Addresses', 'Options']))

@lspcli.command()
@click.argument('uid', required=True)
@click.pass_obj
def get(obj: SkyNetCtxt, uid: str) -> None:
    """
    Get Logical Switch Port Details
    """
    lsp = LSPProvider(obj).get(uid)

    sprint = SeriesPrinter()
    if lsp.lsp.is_empty():
        print('Logical Switch Port not found')
        return

    print(sprint.print(lsp.lsp.data().iloc[0]))
    print('Logical Switch:')
    if lsp.ls.is_empty():
        print("no info available")
    else:
        print(sprint.print(lsp.ls.data().iloc[0], 4))

    if not lsp.pod.is_empty():
        print('Pod:')
        print(sprint.print(lsp.pod.data().iloc[0], 4))

    if not lsp.iface.is_empty():
        print('Interface:')
        print(sprint.print(lsp.iface.data().iloc[0], 4))

    if not lsp.lrp.is_empty():
        print('Logical Router Port:')
        print(sprint.print(lsp.lrp.data().iloc[0], 4))

