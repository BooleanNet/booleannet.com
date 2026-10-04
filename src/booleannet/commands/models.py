#!/usr/bin/env python3
"""List models or print one model in a chosen format.

    bnet models                 one summary row per model
    bnet models 1               bnet for model 001
    bnet models 1 -f aeon       aeon for model 001
    bnet models -d models.json  read a chosen JSON database
"""

import gzip
import json
import sys
from importlib.resources import files
from pathlib import Path

import click

DATA = files("booleannet").joinpath("data", "models.json.gz")
FORMATS = (
    "bnet",
    "booleannet",
    "sbml",
    "aeon",
    "bma",
    "inferred_graph",
    "metadata",
    "readme",
)
JSON_FORMATS = {"bma", "metadata"}


def load_models(path: Path | None):
    if path is None:
        with DATA.open("rb") as raw, gzip.open(raw, "rt") as f:
            return json.load(f)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as f:
        return json.load(f)


def list_summaries(models):
    rows = []
    for model_id in sorted(models):
        summary = models[model_id]["summary"]
        rows.append((
            model_id,
            summary["name"],
            summary["variables"],
            summary["inputs"],
            summary["regulations"],
        ))
    name_w = max(len(name) for _, name, _, _, _ in rows)
    click.echo(f"{'id':3}  {'name':<{name_w}}  {'var':>5}  {'in':>4}  {'reg':>5}")
    for model_id, name, variables, inputs, regulations in rows:
        click.echo(f"{model_id}  {name:<{name_w}}  {variables:5}  {inputs:4}  {regulations:5}")


def normalize_id(ctx, param, value):
    if value is None:
        return None
    if not value.isdigit():
        raise click.BadParameter("must be an integer")
    return value.zfill(3)


def emit(model, fmt):
    value = model[fmt]
    if fmt in JSON_FORMATS:
        click.echo(json.dumps(value, ensure_ascii=False))
        return
    click.echo(value, nl=not value.endswith("\n"))


@click.command()
@click.argument("model_id", required=False, callback=normalize_id)
@click.option(
    "-d",
    "--database",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="JSON or JSON.gz database. Default: packaged data/models.json.gz.",
)
@click.option(
    "-f",
    "--format",
    "fmt",
    default="bnet",
    show_default=True,
    type=click.Choice(FORMATS),
    help="Model file to print when MODEL_ID is given.",
)
def main(model_id, database, fmt):
    """List model summaries, or print one model in the chosen format."""
    models = load_models(database)
    if model_id is None:
        list_summaries(models)
        return

    if model_id not in models:
        raise click.ClickException(f"no model {model_id}")
    emit(models[model_id], fmt)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stdout.close()
        sys.exit(0)
