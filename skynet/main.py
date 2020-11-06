import click
import logging

from skynet.context import SkyNetCtxt
from skynet.ovn.cli import ovncli
from skynet.ovs.cli import ovscli
from skynet.node.cli import nodecli


@click.group()
@click.option(
    '--at',
    help='Specify a time in the past.'
    'Allowed formats: timestamp, RFC1123, Go Duration Format'
    'Examples: "-1.5h", "-200ms", "Sun, 06 Nov 2016 08:49:37 GMT", "1479899809"'
)
@click.option(
    '--log',
    '-l',
    help='Set log level [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
    default="INFO"
)
@click.pass_context
def maincli(ctx, at: str = None, log: str = "INFO"):
    """
    Sky Net Utility
    """
    ctx.obj = SkyNetCtxt()
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
