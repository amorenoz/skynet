import click

from skynet.context import SkyNetCtxt
from skynet.k8s.data import K8sProvider, K8sFilter


@click.group(name='k8s')
@click.pass_obj
def k8scli(obj: SkyNetCtxt) -> None:
    """
    Kubernetes Commands
    """
    pass


@click.group(name='pod')
@click.pass_obj
def podcli(obj: SkyNetCtxt) -> None:
    """
    Pod Commands
    """
    pass


@podcli.command(name='list')
@click.argument('filter', required=False, default="")
@click.pass_obj
def listpods(obj: SkyNetCtxt, filter: str) -> None:
    """
    List Pods


    \b
    FILTER is a Filter string formatted as "Filter1=Value1,Filter2=Value2,..."
    Supported Filters:
        Namespace   [Namespace]
    """
    filter_obj = K8sFilter()
    filter_obj.process_string(filter)
    print(
        K8sProvider(obj).list_pods(filter_obj).to_string([
            'Namespace', 'Name', 'Status', 'Node', 'IP', 'HostNetwork',
            'HostIP'
        ]))


@click.group(name='container')
@click.pass_obj
def containercli(obj: SkyNetCtxt) -> None:
    """
    Container Commands
    """
    pass


@containercli.command(name='list')
@click.argument('filter', required=False, default="")
@click.pass_obj
def listcontainers(obj: SkyNetCtxt, filter: str) -> None:
    """
    List Containers


    \b
    FILTER is a Filter string formatted as "Filter1=Value1,Filter2=Value2,..."
    Supported Filters:
        Namespace   [Namespace]
        Pod         [Pod]
    """
    filter_obj = K8sFilter()
    filter_obj.process_string(filter)
    print(
        K8sProvider(obj).list_containers(filter_obj).to_string(
            ['Namespace', 'Name', 'Pod', 'Ports']))


k8scli.add_command(podcli)
k8scli.add_command(containercli)
