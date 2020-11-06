import click
import sys
from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.ovs.flows.data import OFFLowData, OFFlowProvider


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

    processed_filter = process_flow_filter(filter) if filter else {}
    flows = OFFlowProvider(obj).get(processed_filter)
    if format == "text":
        print(flows.to_text())
    elif format == "json":
        print(flows.to_json())
    elif format == "html":
        print(flows.to_html())
    elif format == "ovs":
        print(flows.to_ovs())


def process_flow_filter(filter_str: str) -> Dict[str, Any]:
    """
    Process incoming filter strings and return a valid filter dictionary
    """
    filters = {"Table": int, "Cookie": str, "Priority": int, "Host": str}

    filter_dict = {}
    for filter_elem in filter_str.split(','):
        filter_parts = filter_elem.split('=')
        if len(filter_parts) != 2:
            raise click.ClickException('Wrong filter format')
        key = filter_parts[0]
        val = filter_parts[1]
        if not key or not val:
            raise click.ClickException('Wrong filter format')
        if key not in filters.keys():
            raise click.ClickException('Unsupported filter %s' % key)

        filter_dict[key] = filters[key](val)
    return filter_dict


ovscli.add_command(flowscli)
