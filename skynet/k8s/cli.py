import click

from skynet.common.printers import SeriesPrinter
from skynet.context import SkyNetCtxt
from skynet.k8s.data import K8sProvider, K8sFilter


@click.group(name='k8s')
@click.pass_obj
def k8scli(obj: SkyNetCtxt) -> None:
    """
    Kubernetes Commands
    """


@click.group(name='pod')
@click.pass_obj
def podcli(obj: SkyNetCtxt) -> None:
    """
    Pod Commands
    """


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


@podcli.command(name='get')
@click.argument('uid', required=True)
@click.pass_obj
def getpod(obj: SkyNetCtxt, uid: str) -> None:
    """
    List Pods

    \b
    POD must be the UID of a pod
    """
    pod = K8sProvider(obj).get_pod(uid)

    sprint = SeriesPrinter()
    if pod.pod.is_empty():
        print('Pod not found')
        return

    print(sprint.print(pod.pod.data().iloc[0]))
    print('Containers:')
    if pod.containers.is_empty():
        print("no info available")
    else:
        for _, container in pod.containers.data().iterrows():
            print(sprint.print(container, 4))
    print('Logical Switch Port:')
    if pod.lsp.is_empty():
        print("no info available")
    else:
        print(sprint.print(pod.lsp.data().iloc[0], 4))
    print('Veth Interface ')
    if pod.iface.is_empty():
        print("no info availablle")
    else:
        print(sprint.print(pod.iface.data().iloc[0], 4))


@click.group(name='container')
@click.pass_obj
def containercli(obj: SkyNetCtxt) -> None:
    """
    Container Commands
    """


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
