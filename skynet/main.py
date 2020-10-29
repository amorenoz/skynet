import click

from skynet.context import SkyNetCtxt
from skynet.ovn.cli import ovncli


@click.group()
@click.pass_context
def maincli(ctx):
    """
    Sky Net Utility
    """
    ctx.obj = SkyNetCtxt()


def main():
    """
    Main Function
    """
    maincli()


maincli.add_command(ovncli)
