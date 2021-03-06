import click
import logging

from skynet.context import SkyNetCtxt
from skynet.ovn.cli import ovncli
from skynet.ovs.cli import ovscli
from skynet.node.cli import nodecli
from skynet.summary import summary
from skynet.host.cli import hostcli
from skynet.k8s.cli import k8scli
from skynet.capture.cli import capturecli


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    '--at',
    help='Specify a time in the past.'
    'Allowed formats: timestamp, RFC1123, Go Duration Format'
    'Examples: "-1.5h", "-200ms", "Sun, 06 Nov 2016 08:49:37 GMT"'
    '"1479899809"'
)
@click.option('--log',
              '-l',
              help='Set log level [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
              default="INFO")
@click.option('--api',
              '-a',
              help='Skydive API: IP:PORT.'
              'E.g: localhost:8082, 172.10.10.45:8082',
              default="localhost:8082")
@click.pass_context
def maincli(ctx,
            at: str = None,
            log: str = "INFO",
            api: str = "localhost:8082"):
    """
    Sky Net Utility
    """
    ctx.obj = SkyNetCtxt(api)
    if at:
        ctx.obj.set_option("at", at)

    if log:
        logging.basicConfig(level=log)


def main():
    """
    Main Function
    """
    maincli()


maincli.add_command(ovncli)
maincli.add_command(ovscli)
maincli.add_command(nodecli)
maincli.add_command(hostcli)
maincli.add_command(summary)
maincli.add_command(k8scli)
maincli.add_command(capturecli)
