import click
import json

from hulse import utils


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.option(
    "--key", metavar="API_KEY", help="API key for the Hulse server", required=True
)
def host(key):
    """Run the Hulse host.

    :param key: Hulse API key.
    :type key: str
    """
    click.echo(f"Starting your Hulse host 🚀 🛠 🔭!")
    utils.run_host(api_key=key)


@cli.command()
@click.option(
    "--key", metavar="API_KEY", help="API key for the Hulse server", required=True
)
def clusters(key):
    """Get all clusters."""
    clusters = utils.get_clusters(api_key=key)
    click.echo(f"Here are your clusters:\n\n\n{json.dumps(clusters, indent=2)}")
