#!/usr/bin/env python3
"""
Convert BBM models files to a JSON data file.

Join models/summary.csv to each model directory and write one JSON object.

Directory names follow the summary columns (regulations is not in the name):

    [id-009]__[var-60]__[in-13]__[YEAST-APOPTOSIS]

The output is a JSON object keyed by the zero-padded id from the CSV:

    {
      "009": {
        "summary": {
          "name": "YEAST-APOPTOSIS",
          "variables": 60,
          "inputs": 13,
          "regulations": 114
        },
        "metadata": { ... },          # metadata.json, parsed
        "readme": "...",              # README.md
        "bnet": "...",                # model.bnet
        "aeon": "...",                # model.aeon
        "sbml": "...",                # model.sbml
        "bma": { ... },               # model.bma.json, parsed
        "booleannet": "...",          # model.booleannet.txt
        "inferred_graph": "..."       # model.inferred-graph.aeon
      }
    }

JSON files are stored as objects. The other formats stay as text.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

DIR_RE = re.compile(
    r"^\[id-(?P<id>\d+)\]__\[var-(?P<variables>\d+)\]__\[in-(?P<inputs>\d+)\]__\[(?P<name>.+)\]$"
)

# filename -> (output field, "json" or "text")
FILES = {
    "metadata.json": ("metadata", "json"),
    "README.md": ("readme", "text"),
    "model.bnet": ("bnet", "text"),
    "model.aeon": ("aeon", "text"),
    "model.sbml": ("sbml", "text"),
    "model.bma.json": ("bma", "json"),
    "model.booleannet.txt": ("booleannet", "text"),
    "model.inferred-graph.aeon": ("inferred_graph", "text"),
}


def read_summary(path):
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f, skipinitialspace=True))
    by_id = {}
    for row in rows:
        model_id = row["ID"].zfill(3)
        if model_id in by_id:
            raise SystemExit(f"duplicate id {model_id} in {path}")
        by_id[model_id] = {
            "name": row["name"],
            "variables": int(row["variables"]),
            "inputs": int(row["inputs"]),
            "regulations": int(row["regulations"]),
        }
    return by_id


def index_dirs(models_dir):
    by_id = {}
    for path in sorted(models_dir.iterdir()):
        if not path.is_dir():
            continue
        match = DIR_RE.match(path.name)
        if not match:
            raise SystemExit(f"directory name does not match summary pattern: {path.name}")
        model_id = match.group("id").zfill(3)
        if model_id in by_id:
            raise SystemExit(f"duplicate id {model_id}: {path.name}")
        by_id[model_id] = (path, match.groupdict())
    return by_id


def load_files(directory):
    data = {}
    for filename, (field, kind) in FILES.items():
        path = directory / filename
        if not path.is_file():
            raise SystemExit(f"missing {path}")
        text = path.read_text()
        data[field] = json.loads(text) if kind == "json" else text
    return data


def build(summary, dirs):
    if set(summary) != set(dirs):
        missing = sorted(set(summary) - set(dirs))
        extra = sorted(set(dirs) - set(summary))
        raise SystemExit(f"summary/directory mismatch missing={missing} extra={extra}")

    models = {}
    for model_id in sorted(summary):
        row = summary[model_id]
        path, parsed = dirs[model_id]
        parsed_vars = int(parsed["variables"])
        parsed_inputs = int(parsed["inputs"])
        if (
            parsed["name"] != row["name"]
            or parsed_vars != row["variables"]
            or parsed_inputs != row["inputs"]
        ):
            raise SystemExit(
                f"id {model_id} summary {row} does not match directory {path.name}"
            )
        models[model_id] = {
            "summary": row,
            **load_files(path),
        }
    return models


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--summary", type=Path, default=root / "models" / "summary.csv")
    parser.add_argument("--models", type=Path, default=root / "models")
    parser.add_argument("-o", "--output", type=Path, default=root / "models.json")
    args = parser.parse_args()

    models = build(read_summary(args.summary), index_dirs(args.models))
    with args.output.open("w") as f:
        json.dump(models, f, ensure_ascii=False, separators=(",", ":"), indent=2)
        f.write("\n")
    print(f"wrote {len(models)} models to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
