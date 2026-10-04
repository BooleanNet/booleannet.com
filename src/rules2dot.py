"""Build a Graphviz interaction graph from BooleanNet rules."""

import re
import shutil
import subprocess
from pathlib import Path

from pyboolnet import log

import click
from pyboolnet.boolean_normal_forms import functions2primes
from pyboolnet.interaction_graphs import (
    add_style_interactionsigns,
    igraph2dot,
    primes2igraph,
)

KEYWORDS = {"and", "or", "not", "True", "False"}
ENGINES = ("dot", "neato", "fdp", "sfdp", "circo", "twopi")
IDENT = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")


def booleannet2functions(text: str) -> dict:
    """Turn BooleanNet update rules into callables for pyboolnet.

    Parameter names are sorted because functions2primes calls each
    function with arguments in alphabetical order.
    """
    funcs = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        lhs, rhs = line.split("=", 1)
        name = lhs.strip().removesuffix("*").strip()
        expr = rhs.strip()
        args = sorted(set(IDENT.findall(expr)) - KEYWORDS)
        params = ", ".join(args)
        src = f"lambda {params}: {expr}" if args else f"lambda: {expr}"
        funcs[name] = eval(src, {"True": True, "False": False})
    return funcs


def rules2dot(rules_path: Path, dot_path: Path) -> None:
    primes = functions2primes(booleannet2functions(rules_path.read_text()))
    graph = primes2igraph(primes)
    # Default width is ~0.2in for one-letter names, which clips the labels.
    graph.graph["node"]["width"] = "0.55"
    graph.graph["node"]["fontsize"] = "14"
    graph.graph["node"]["color"] = "gray20"
    graph.graph["node"]["penwidth"] = "1.4"
    # width is a minimum; let longer labels expand the circle
    graph.graph["node"]["fixedsize"] = "false"
    for name in graph.nodes:
        if name.startswith("v_"):
            graph.nodes[name]["label"] = name.removeprefix("v_")
    add_style_interactionsigns(graph)
    igraph2dot(graph, str(dot_path))


def write_image(dot: Path, image: Path, engine: str = "neato") -> None:
    """Render a dot file. The image format is the output suffix, such as png or pdf.

    pyboolnet's layout lookup is hardcoded to /usr/bin, so this calls the engine on PATH.
    """
    exe = shutil.which(engine)
    if exe is None:
        raise click.ClickException(f"{engine} not found on PATH")
    fmt = image.suffix.lstrip(".").lower()
    if not fmt:
        raise click.ClickException(f"image path needs an extension such as .png or .pdf: {image}")
    subprocess.run([exe, f"-T{fmt}", str(dot), "-o", str(image)], check=True)
    log.info(f"image written to {image}")


@click.command(no_args_is_help=True)
@click.option("-i", "--input", "rules", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path), help="BooleanNet rules file.")
@click.option("-d", "--dot", "dot", type=click.Path(dir_okay=False, path_type=Path), help="Dot output. Default: input path with a .dot suffix.")
@click.option("-o", "--output", "image", type=click.Path(dir_okay=False, path_type=Path), help="Image output. Default: input path with a .png suffix. Format follows the extension (png, pdf, svg).")
@click.option("-e", "--engine", default="neato", show_default=True, type=click.Choice(ENGINES), help="Graphviz layout engine.")
def main(rules: Path, dot: Path | None, image: Path | None, engine: str) -> None:
    dot = dot or rules.with_suffix(".dot")
    image = image or rules.with_suffix(".png")
    rules2dot(rules, dot)
    write_image(dot, image, engine)


if __name__ == "__main__":
    main()
