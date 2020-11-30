import click
from graphviz import Digraph
from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.ovn.lr.cli import lrcli
from skynet.ovn.ls.cli import lscli
from skynet.ovn.acl.cli import aclcli
from skynet.ovn.lrp.cli import lrpcli
from skynet.ovn.lsp.cli import lspcli
from skynet.ovn.datapath.cli import datapathcli
from skynet.ovn.lflow.cli import lflowcli


@click.group(name='ovn')
@click.pass_obj
def ovncli(obj: SkyNetCtxt) -> None:
    """
    OVN command
    """
    pass


@ovncli.command()
@click.option('-n',
              '--namespace',
              default='default',
              show_default=True,
              type=str,
              help='Kubernetes namespace to plot')
@click.pass_obj
def topology(obj: SkyNetCtxt, namespace: str) -> None:
    """
    Print the OVN logical topology (.dot format)
    """
    graph = obj.rest_cli().lookup(
        "G.V().Has('Manager', 'ovn', 'Type', Within('logical_switch', 'logical_switch_port', 'logical_router', 'logical_router_port', 'acl'))."
        "As('ovn').g.V().Has('Type', Within('pod')).Has('K8s.Namespace', '{name}').As('k8s').Select('ovn','k8s').Subgraph()"
        .format(name=namespace))
    dot = topo2dot('OVN Topology', graph[0])
    print(dot)


def topo2dot(name: str, graph: Dict[str, List[Any]]) -> Digraph:
    """
    Transform a topology graph into a Digraph object
    """
    dot = Digraph(name=name)

    for node in graph.get('Nodes') or []:
        attr = {}
        if node['Metadata']['Type'] == 'logical_router':
            attr['shape'] = 'box'
            attr['style'] = 'filled'
            attr['color'] = 'lightgrey'
        elif node['Metadata']['Type'] == 'logical_switch':
            attr['shape'] = 'box'
        elif node['Metadata']['Type'] == 'acl':
            continue
        elif node['Metadata']['Type'] == 'pod':
            attr['style'] = 'filled'
            attr['color'] = 'lightblue2'

        label = "({}) {}".format(node['Metadata']['Type'],
                                 node['Metadata']['Name'])

        dot.node(node['ID'], label, **attr)

    for edge in graph.get('Edges') or []:
        dot.edge(edge['Parent'], edge['Child'])

    return dot


ovncli.add_command(lrcli)
ovncli.add_command(lscli)
ovncli.add_command(aclcli)
ovncli.add_command(lrpcli)
ovncli.add_command(lspcli)
ovncli.add_command(datapathcli)
ovncli.add_command(lflowcli)
