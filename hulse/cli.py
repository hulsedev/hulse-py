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
def get_clusters(key):
    """Get all clusters for the given account.

    :param key: Hulse api key.
    :type key: str
    """
    clusters = utils.get_clusters(api_key=key)
    click.echo(f"Here are your clusters:\n\n\n{json.dumps(clusters, indent=2)}")


@cli.command()
@click.option(
    "--key", metavar="API_KEY", help="API key for the Hulse server", required=True
)
@click.option("--name", metavar="NAME", help="Name of the cluster", required=True)
@click.option(
    "--description",
    metavar="DESCRIPTION",
    help="Description of the cluster",
    required=False,
    default=None,
)
def create_cluster(key, name, description):
    """Create a new Hulse cluster

    :param key: Hulse api key.
    :type key: str
    :param name: Name of the newly created cluster.
    :type name: str
    :param description: Description of the cluster (purpose, characteristics).
    :type description: str
    """

    was_created = utils.create_cluster(api_key=key, name=name, description=description)
    if was_created:
        click.echo(f"Successfully created cluster {name} 🎈🍰🍾!")
    else:
        click.echo(f"Failed to create cluster {name} 😢")
