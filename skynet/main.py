import click
from skydive.rest.client import RESTClient

import skynet.ovn.cli


@click.group()
@click.pass_context
def maincli(ctx):
    ctx.obj = RESTClient("localhost:8082")


def main():
    maincli()


maincli.add_command(skynet.ovn.cli.ovncli)
