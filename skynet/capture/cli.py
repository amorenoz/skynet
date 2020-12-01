import click
from typing import Dict, List, Any

from skynet.context import SkyNetCtxt
from skynet.capture.data import CaptureProvider


@click.group(name='capture')
@click.pass_obj
def capturecli(obj: SkyNetCtxt) -> None:
    """
    Create and visualize packet captures
    """
    pass


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
@click.argument('interface', required=True)
@click.pass_obj
def create(obj: SkyNetCtxt, bpf: str, description: str, name: str,
           interface: str) -> None:
    """
    Create a new capture

    \b
    INTERFACE is the name of the OvS interface to capture from
    """
    prov = CaptureProvider(obj)
    print(prov.create(bpf, name, description, interface).data())


@capturecli.command()
@click.argument('capture', required=True)
@click.pass_obj
def get(obj: SkyNetCtxt, capture: str) -> None:
    """
    Get a Capture information (flows)

    \b
    CAPTURE is the ID of the capture
    """
    prov = CaptureProvider(obj)
    flows = prov.get(capture)
    if not flows.is_empty():
        print(flows.data().to_string())


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
