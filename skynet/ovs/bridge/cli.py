import click
import textwrap

from skynet.context import SkyNetCtxt
from skynet.ovs.bridge.data import OvSDataProvider


@click.group(name='bridge')
@click.pass_obj
def bridgecli(obj: SkyNetCtxt) -> None:
    """
    OvS Bridge commands
    """
    pass


@bridgecli.command()
@click.option('-h',
              '--host',
              'host',
              help='Only list the OvS Bridges on a host'
              '(Either name or UUID are acceptable values)')
@click.pass_obj
def list(obj: SkyNetCtxt, host: str) -> None:
    """
    List OvS Bridges
    """
    print(
        OvSDataProvider(obj).list_bridges(host).to_string(
            columns=['Host', 'Name', 'BridgeID', 'BridgeUplink']))


@bridgecli.command(name='get')
@click.argument('bridge', required=True)
@click.pass_obj
def get_bridge(obj: SkyNetCtxt, bridge: str) -> None:
    """
    Get detail information from a bridge
    """
    iface_info = {
        'internal': ['Type', 'Name', 'IPV4'],
        'patch': ['Type', 'Name', 'Peer', 'LocalPort'],
        'geneve':
        ['Type', 'Name', 'MTU', 'TunEgressIface', 'TunEgressIfaceCarrier'],
        'veth': [
            'Type', 'Name', 'State', 'IPAddress', 'AttachedMAC', 'Sandbox',
            'IfaceID'
        ],
    }
    indent_str = ' '

    ovsbridge = OvSDataProvider(obj).get_bridge(bridge)
    print(ovsbridge.bridge.data()[['Name', 'BridgeID']].iloc[0])
    print("Ports:")
    for port in ovsbridge.ports:
        print(
            textwrap.indent(port.port.data()[['Name']].iloc[0].to_string(),
                            indent_str * 4))
        print(textwrap.indent("Interfaces:", indent_str * 4))

        for uid, iface in port.ifaces.data()[['Type']].iterrows():
            series = port.ifaces.data()[iface_info[iface['Type']]].loc[uid]
            print(textwrap.indent(series.to_string(), indent_str * 8))
