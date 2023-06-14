import logging

import click
import genanki
from rich.console import Console
from rich.logging import RichHandler

from ganki import Ganki

# Setup console
console = Console()

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            console=console,
            rich_tracebacks=True,
            markup=True,
            show_time=False,
            show_level=False,
        )
    ],
)

logger = logging.getLogger("rich")


@click.group()
def cli():
    pass


@cli.command()
@click.option("--uri-type", help="Type of URI (file or url)", default="url")
@click.option("--deck-name", help="Name of output anki deck", default="ganki_deck")
@click.option("-o", "--output", help="Output path", default="ganki_deck.apkg")
@click.option("-m", "--model", help="OpenAI Model Name", default="gpt-3.5-turbo")
@click.argument("uri")
def create_deck(uri, uri_type, deck_name, output, model):
    ganki = Ganki(model_name=model)
    f = (
        ganki.create_deck_from_file
        if uri_type == "file"
        else ganki.create_deck_from_url
    )
    deck = f(uri, deck_name)
    genanki.Package(deck).write_to_file(output)
    logger.info(
        f"[green]Saved anki deck to[/green] [blue]{output}[/blue]",
        extra={"markup": True},
    )


if __name__ == "__main__":
    cli()
