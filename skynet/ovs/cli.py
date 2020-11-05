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



def trim(data):
    if len(str(data)) < 50:
        return data

    return "{}...".format(str(data)[0:50])


@ovscli.command()
@click.pass_obj
@click.option('--format',
              '-f',
              default="text",
              help='Specify an alternative output format: [json, html]')
def flows(obj: SkyNetCtxt, format) -> None:
    """
    Show the OVS flows
    """
    flows = OFFlowProvider(obj).get()
    print(format)
    if format == "text":
        print(flows.to_text())
    elif format == "json":
        print(flows.to_json())
    elif format == "html":
        print(flows.to_html())
    elif format == "ovs":
        print(flows.to_ovs())
