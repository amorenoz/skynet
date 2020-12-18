import click
import textwrap

from skynet.context import SkyNetCtxt
from skynet.host.data import HostDataProvider
from skynet.platform import Platform, PlatformProvider
from skynet.ovs.bridge.data import OvSDataProvider


@click.command(name='summary')
@click.pass_obj
def summary(obj: SkyNetCtxt) -> None:
    """
    Prints a summary of the network configuration
    """
    plat_prov = PlatformProvider(obj)
    if plat_prov.platform_type() == Platform.K8S:
        print("-----K8s Config -----")
        conf = plat_prov.get_k8s_conf()
        if conf.is_empty():
            print('Unknown')
        else:
            print(conf.data()[['MTU', 'NetCIDR',
                               'SvcCIDR']].iloc[0].to_string())

    hprov = HostDataProvider(obj)
    hosts = hprov.list()
    if hosts.is_empty():
        return

    print("-----Hosts ({})-----".format(len(hosts.data().index)))
    for uid, host in hosts.data()[[
            'Hostname', 'PlatformFamily', 'PlatformVersion'
    ]].iterrows():
        print(textwrap.indent(host.to_string(), '  '))

        oprov = OvSDataProvider(obj)
        bridges = oprov.list_bridges(uid)
        if bridges.is_empty():
            print("No ovs info")
        else:
            print("  {} OvS bridges".format(len(bridges.data().index)))
            for buid, bridge in bridges.data().iterrows():
                print("    Bridge {}".format(bridge['Name']))
                print("       Ports: {}".format(oprov.get_num_ports(buid)))
                print("       Flows: {}".format(oprov.get_num_flows(buid)))
