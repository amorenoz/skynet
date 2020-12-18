import click

from skynet.context import SkyNetCtxt
from skynet.ovs.flows.data import OFFlowFilter, OFFlowProvider
from skynet.ovs.bridge.cli import bridgecli
import IPython


@click.group(name='ovs')
@click.pass_obj
def ovscli(obj: SkyNetCtxt) -> None:
    """
    OVS command
    """


@click.group(name='flows')
@click.pass_obj
def flowscli(obj: SkyNetCtxt) -> None:
    """
    OVS flows commands
    """


@flowscli.command()
@click.pass_obj
@click.option('--format',
              '-f',
              default="text",
              help='Specify an alternative output format: [ovs, json, html]')
@click.option('--interactive',
              '-i',
              is_flag=True,
              help='Drop an interactive iPython shell')
@click.option('--bridge',
              '-b',
              default="",
              help='Specify a bridge UID or name'
              '(note that the name of the bridge may not be unique)')
@click.option('--host', '-H', default="", help='Specify a host UUID or name')
@click.argument('filter', required=False, default="")
def list(obj: SkyNetCtxt,
         format: str,
         interactive: bool,
         bridge: str = "",
         host: str = "",
         filter: str = "") -> None:
    """
    List the OVS flows

    \b
    FILTER is a Filter string formatted as "Filter1=Value1,Filter2=Value2,..."
    Supported Filters:
        Host        [Hostname]
        Cookie:     [Cookie]
        Table:      [Table Num]
        Priority    [Priority Num]
        Match filters:
            eth_src
            eth_dst
            ipv4_dst
            ipv4_src
            eth_type
            tcp_dst
            tcp_src
            ip_proto
            eth_type
            in_port

    E.g Host=mynode1.cluster,Cookie='0x12334',Table=3
    Host=mynode,in_port=4,ipv4_addr=192.168.1.1
    """
    filter_obj = OFFlowFilter()
    filter_obj.process_string(filter)
    flows = OFFlowProvider(obj).list(host, bridge, filter_obj)
    if format == "text":
        print(flows.to_text())
    elif format == "json":
        print(flows.to_json(orient='records'))
    elif format == "html":
        print(flows.to_html())
    elif format == "ovs":
        print(flows.to_ovs())

    if interactive:
        IPython.embed()


ovscli.add_command(flowscli)
ovscli.add_command(bridgecli)
