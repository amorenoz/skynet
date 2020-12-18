import click

from skynet.context import SkyNetCtxt
from skynet.capture.data import CaptureProvider


@click.group(name='capture')
@click.pass_obj
def capturecli(obj: SkyNetCtxt) -> None:
    """
    Create and visualize packet captures
    """


@capturecli.command()
@click.pass_obj
def list(obj: SkyNetCtxt) -> None:
    """
    List the active captures
    """
    prov = CaptureProvider(obj)
    captures = prov.list()
    if not captures.is_empty():
        print(captures.to_string())


@capturecli.command()
@click.option('--bpf', help='BPF Filter', required=False)
@click.option('--description',
              help='A short description of his capture',
              required=False)
@click.option('--name', help='The name of this capture', required=False)
@click.option('--type',
              'port_type',
              help='The type of port or interface to add the capture from'
              'Supported: [ovsport(default), veth, internal]',
              default='ovsport',
              required=False)
@click.argument('port_name', required=True)
@click.pass_obj
def create(obj: SkyNetCtxt, bpf: str, description: str, name: str,
           port_type: str, port_name: str) -> None:
    """
    Create a new capture

    \b
    PORT_NAME is the name of the OvS Port or interface to capture from
    """
    prov = CaptureProvider(obj)
    print(prov.create(bpf, name, description, port_type, port_name).data())


@capturecli.command()
@click.argument('capture', required=True)
@click.pass_obj
def get(obj: SkyNetCtxt, capture: str) -> None:
    """
    Get a Capture information (flows)

    \b
    CAPTURE is the ID of the capture
    """
    show_cols = [
        'LayersPath',
        'LinkProtocol',
        'LinkSrc',
        'LinkDst',
        'NetworkProtocol',
        'NetworkSrc',
        'NetworkDst',
        'TransportProtocol',
        'TransportSrc',
        'TransportDst',
        'Packets',
        'Bytes',
        'ReturnPackets',
        'ReturnBytes',
        'Application',
    ]

    prov = CaptureProvider(obj)
    flows = prov.get(capture)
    if not flows.is_empty():
        print(flows.data().to_string(columns=show_cols))


@capturecli.command()
@click.argument('capture', required=True)
@click.pass_obj
def delete(obj: SkyNetCtxt, capture: str) -> None:
    """
    Delete a Capture

    \b
    CAPTURE is the ID of the capture
    """
    prov = CaptureProvider(obj)
    prov.delete(capture)
