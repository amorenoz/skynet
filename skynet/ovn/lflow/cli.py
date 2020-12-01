import click

from skynet.context import SkyNetCtxt
from skynet.ovn.lflow.data import LFlowProvider, LFlowFilter
from skynet.ovn.lflow.ovn_printer import OVNFLowPrinter
from skynet.common.printers import SeriesPrinter


@click.group(name='lflow')
@click.pass_obj
def lflowcli(obj: SkyNetCtxt) -> None:
    """
    Logical Flow commands
    """
    pass


@lflowcli.command()
@click.pass_obj
@click.option(
    '--format',
    '-f',
    default="table",
    help='Specify an output format: [table (default), text, json, html, ovn]')
@click.argument('filter', required=False, default="")
def list(obj: SkyNetCtxt, filter: str = "", format: str = "table") -> None:
    """
    List Logical Flows

    \b
    FILTER is a Filter string formatted as "Filter1=Value1,Filter2=Value2,..."
    Supported Filters:
        Datapath    [datapath] (full or first 8bytes)
        Table       [tableNum] (table number)
        Pipeline    [Pipeline string]
        Match       [Match Regex]
        Actions     [Actions Regex]
    E.g: Datapath=c51244a5-1620-4a7a-ae1e-c4b882e46aae
         Datapath=c51244a5,Table=12,Match='eth.src == c2.*'
         Actions='drop;'

    """
    filter_obj = LFlowFilter()
    filter_obj.process_string(filter)
    flow_data = LFlowProvider(obj).list(filter_obj)
    if not flow_data.is_empty():
        if not format or format == "table":
            print(flow_data.data().to_string(columns=[
                'Match', 'Actions', 'Pipeline', 'Priority', 'Table', 'Datapath'
            ],
                                             justify="left",
                                             max_colwidth=60))
        elif format == "text":
            sp = SeriesPrinter()
            for _, series in flow_data.data().iterrows():
                print(sp.print(series))
        elif format == "json":
            print(flow_data.data().to_json(orient='records'))
        elif format == "html":
            print(flow_data.data().to_html())
        elif format == "ovn":
            fp = OVNFLowPrinter()
            print(fp.fformat_all(flow_data))
