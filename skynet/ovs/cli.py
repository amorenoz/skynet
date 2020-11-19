import click
import sys
from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.ovs.flows.data import OFFLowData, OFFlowProvider, OFFlowFilter


@click.group(name='ovs')
@click.pass_obj
def ovscli(obj: SkyNetCtxt) -> None:
    """
    OVS command
    """
    pass


@click.group(name='flows')
@click.pass_obj
def flowscli(obj: SkyNetCtxt) -> None:
    """
    OVS flows commands
    """
    pass


@flowscli.command()
@click.pass_obj
@click.option('--format',
              '-f',
              default="text",
              help='Specify an alternative output format: [json, html]')
@click.argument('filter', required=False, default="")
def list(obj: SkyNetCtxt, format, filter: str = "") -> None:
    """
    List the OVS flows

    \b
    FILTER is a Filter string formatted as "Filter1=Value1,Filter2=Value2,..."
    Supported Filters:
        Host        [Hostname]
        Cookie:     [Cookie]
        Table:      [Table Num]
        Priority    [Priority Num]
    E.g Host=mynode1.cluster,Cookie='0x12334',Table=3
    """
    filter_obj = OFFlowFilter()
    filter_obj.process_string(filter)
    flows = OFFlowProvider(obj).list(filter_obj)
    if format == "text":
        print(flows.to_text())
    elif format == "json":
        print(flows.to_json())
    elif format == "html":
        print(flows.to_html())
    elif format == "ovs":
        print(flows.to_ovs())

ovscli.add_command(flowscli)
