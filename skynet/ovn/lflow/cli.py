import click

from skynet.context import SkyNetCtxt
from skynet.ovn.lflow.data import LFlowProvider, LFlowFilter


@click.group(name='lflow')
@click.pass_obj
def lflowcli(obj: SkyNetCtxt) -> None:
    """
    Logical Flow commands
    """
    pass


@lflowcli.command()
@click.pass_obj
@click.argument('filter', required=False, default="")
def list(obj: SkyNetCtxt, filter: str = "") -> None:
    """
    List Logical Flows

    \b
    FILTER is a Filter string formatted as "Filter1=Value1,Filter2=Value2,..."
    Supported Filters:
        Datapath    [datapath] (full or first 8bytes)
        Table       [tableNum] (table number)
        Match       [Match Regex]
        Actions     [Actions Regex]
    E.g: Datapath=c51244a5-1620-4a7a-ae1e-c4b882e46aae
         Datapath=c51244a5,Table=12,Match='eth.src == c2.*'
         Actions='drop'

    """
    filter_obj = LFlowFilter()
    filter_obj.process_string(filter)
    flow_data = LFlowProvider(obj).list(filter_obj)
    if not flow_data.is_empty():
        print(flow_data.data().to_string(columns=[
            'Match', 'Actions', 'Pipeline', 'Priority', 'Table', 'Datapath'
        ],
                                         justify="left",
                                         max_colwidth=60))
