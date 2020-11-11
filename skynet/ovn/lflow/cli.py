import click

from skynet.context import SkyNetCtxt
from skynet.ovn.lflow.data import LFlowProvider


@click.group(name='lflow')
@click.pass_obj
def lflowcli(obj: SkyNetCtxt) -> None:
    """
    Logical Flow commands
    """
    pass


@lflowcli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List Logical Flows
    """
    print(
        LFlowProvider(obj).get().data().to_string(
            columns=['Match', 'Actions', 'Pipeline','Priority', 'Table', 'DataPath'],
            justify="left",max_colwidth=65))
