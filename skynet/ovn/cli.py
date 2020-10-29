import click
from graphviz import Digraph
from typing import Dict, List, Any

from skynet.context import SkyNetCtxt


@click.group(name='ovn')
@click.pass_obj
def ovncli(obj) -> None:
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
    Show the OVN logical topology
    """
    graph = obj.rest_cli().lookup(
        "g.V().Has('Manager', 'ovn').As('ovn').g.V().Has('Type', Within('pod')).Has('K8s.Namespace', '{name}').As('k8s').Select('ovn','k8s').Subgraph()"
        .format(name=namespace))
    dot = topo2dot('OVN Topology', graph[0])
    dot.view()


def topo2dot(name: str, graph: Dict[str, List[Any]]) -> Digraph:
    """
    Transform a topology graph into a Digraph object
    """
    dot = Digraph(name=name)

    for node in graph.get('Nodes'):
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
    for edge in graph.get('Edges'):
        dot.edge(edge['Parent'], edge['Child'])

    return dot
