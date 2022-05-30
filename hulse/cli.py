import click
import json
import webbrowser
import time

from hulse import utils, settings, errors


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
def host():
    """Run the Hulse host."""
    if not settings.CONFIG.get("api_key"):
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first."
        )
    else:
        click.echo(f"Starting your Hulse host 🚀 🛠 🔭!")
        utils.run_host(api_key=settings.CONFIG.get("api_key"))


@cli.command()
def login():
    """Running the Hulse login."""
    if settings.CONFIG.get("api_key"):
        click.echo("You are already logged in 🙂. To log out, run `hulse logout`.")
    else:
        # start a login thread, wait for user to login from terminal
        login_thread = utils.LoginThread()
        login_thread.start()
        click.echo(
            f"Waiting for you to login 😴. Visit: {settings.HULSE_LOGIN_URL} to log in to your Hulse account."
        )
        webbrowser.open_new(settings.HULSE_LOGIN_URL)
        while not login_thread.get_api_key():
            time.sleep(0.1)

        # stop login thread
        login_thread.raise_exception(SystemExit)
        login_thread.join()

        # set & save config for future use
        was_set = settings.set_config(
            dict(
                api_key=login_thread.get_api_key(),
                username=login_thread.get_username(),
                email=login_thread.get_email(),
            )
        )
        if not was_set:
            click.echo(
                "Ouch! We failed to finalize your log in 😧. Please try again by running `hulse login`.",
                err=True,
            )
        else:
            click.secho(
                f"\nWelcome {settings.CONFIG.get('email')} 👋! You logged in successfully 🥳 🦦 🚀!",
                bold=True,
            )


@cli.command()
def logout():
    """Running the Hulse logout."""
    if settings.CONFIG.get("api_key"):
        settings.reset_config()
        click.secho("You have successfully logged out. 👋", bold=True)
    else:
        click.echo("You are not logged in 😢. To log in, run `hulse login`.")


@cli.command()
def tasks():
    click.echo(f"Hulse supports the following tasks 🦠:")
    click.echo(json.dumps(settings.SUPPORTED_TASKS, indent=4))


@cli.command()
def get_clusters():
    """Get all clusters for the given account."""
    if not settings.CONFIG.get("api_key"):
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first.",
        )
    else:
        clusters = utils.get_clusters(api_key=settings.CONFIG.get("api_key"))
        click.echo(f"Here are your clusters 🍜:\n{json.dumps(clusters, indent=4)}")


@cli.command()
@click.option("--name", metavar="NAME", help="Name of the cluster", required=True)
@click.option(
    "--description",
    metavar="DESCRIPTION",
    help="Description of the cluster",
    required=False,
    default=None,
)
def create_cluster(name, description):
    """Create a new Hulse cluster

    :param name: Name of the newly created cluster.
    :type name: str
    :param description: Description of the cluster (purpose, characteristics).
    :type description: str
    """
    if not settings.CONFIG.get("api_key"):
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first."
        )
    else:
        try:
            was_created = utils.create_cluster(
                api_key=settings.CONFIG.get("api_key"),
                name=name,
                description=description,
            )
        except Exception as e:
            was_created = False

        if was_created:
            click.secho(f"Successfully created cluster {name} 🎈🍰🍾!", bold=True)
        else:
            click.echo(f"Failed to create cluster {name} 😢")


@cli.command()
@click.option(
    "--cluster-id", metavar="CLUSTER_ID", help="Id of the cluster", required=True
)
def join_cluster(cluster_id):
    if not settings.CONFIG.get("api_key"):
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first."
        )
    else:
        try:
            was_joined = utils.join_cluster(
                cluster_id=cluster_id, api_key=settings.CONFIG.get("api_key")
            )
        except errors.HulseError as e:
            was_joined = False

        if was_joined:
            click.echo(f"Successfully joined cluster {cluster_id} 🎈 🍰 🍾!")
        else:
            click.echo(
                f"Failure to join cluster {cluster_id} 😢. Try again or visit your Hulse dashboard."
            )


@cli.command()
@click.option(
    "--cluster-id", metavar="CLUSTER_ID", help="Id of the cluster", required=True
)
def leave_cluster(cluster_id):
    if not settings.CONFIG.get("api_key"):
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first."
        )
    else:
        try:
            left = utils.leave_cluster(
                cluster_id=cluster_id, api_key=settings.CONFIG.get("api_key")
            )
        except errors.HulseError as e:
            left = False

        if left:
            click.echo(f"Successfully left cluster {cluster_id} 🎈 🍰 🍾!")
        else:
            click.echo(
                f"Failure to leave cluster {cluster_id} 😢. Try again or visit your Hulse dashboard."
            )


@cli.command()
@click.option(
    "--cluster-id", metavar="CLUSTER_ID", help="Id of the cluster", required=True
)
@click.option("--name", metavar="NAME", help="New name of the cluster", required=True)
@click.option(
    "--description", metavar="DESCRIPTION", help="New description of the cluster"
)
def edit_cluster(cluster_id, name, description):
    if not settings.CONFIG.get("api_key"):
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first."
        )
    else:
        try:
            was_edited = utils.edit_cluster(
                cluster_id=cluster_id,
                name=name,
                description=description,
                api_key=settings.CONFIG.get("api_key"),
            )
        except errors.HulseError as e:
            was_edited = False

        if was_edited:
            click.echo(f"Successfully edited cluster {cluster_id} 🎈 🍰 🍾!")
        else:
            click.echo(
                f"Failed to edit cluster {cluster_id} 😢. Try again or visit your Hulse dashboard."
            )


@cli.command()
@click.option(
    "--cluster-id", metavar="CLUSTER_ID", help="Id of the cluster", required=True
)
def delete_cluster(cluster_id):
    if not settings.CONFIG.get("api_key"):
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first."
        )
    else:
        try:
            was_deleted = utils.delete_cluster(
                cluster_id=cluster_id, api_key=settings.CONFIG.get("api_key")
            )
        except errors.HulseError as e:
            was_deleted = False

        if was_deleted:
            click.secho(f"Successfully deleted cluster {cluster_id} ⌫!")
        else:
            click.echo(
                f"Failed to delete cluster {cluster_id} 😢. Try again or visit your Hulse dashboard."
            )


@cli.command()
def invite_user():
    """Invite user to join a cluster"""
    pass


@cli.command()
@click.option("--api-key", prompt="🔑 Enter your API key", type=str)
@click.option(
    "--username", prompt="📝 Enter your username (optional)", type=str, required=False
)
@click.option("--email", prompt="📧 Enter your email", type=str)
def init(api_key, username, email):
    """Manually set login variables rather using the `hulse login` command."""
    if settings.CONFIG.get("api_key"):
        click.echo("You are already logged in 🙂. To log out, run `hulse logout`.")
    else:
        was_set = settings.set_config(
            dict(
                api_key=api_key,
                username=username,
                email=email,
            )
        )

        if not was_set:
            click.echo(
                "Ouch! We failed to finalize your log in 😧. Please try again by running `hulse login`.",
                err=True,
            )
        else:
            click.secho(
                f"\nWelcome {settings.CONFIG.get('email')} 👋! You logged in successfully 🥳 🦦 🚀!",
                bold=True,
            )


@cli.command()
def get_api_key():
    """Get the current API key."""
    if settings.CONFIG.get("api_key"):
        click.echo(f"Your API key is 🔑: {settings.CONFIG.get('api_key')}")
    else:
        click.echo(
            f"It seems like you're not logged in 😢. Please run `hulse login` first."
        )
