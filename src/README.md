# BooleanNet

BooleanNet is a training tool for managing existing tools and models.

It is not a package that implements new modeling techniques or algorithms.

## Installation

```bash
pip install booleannet
```

It installs the bnet command line tool that implements a number of subcommands.

## Usage

```bash
# List all models
bnet models
```

prints:

```
id   name                                                   var    in    reg
001  SIGNALING-IN-MACROPHAGE-ACTIVATION                     302    19    533
002  SIGNAL-TRANSDUCTION-IN-FIBROBLASTS                     130     9    557
003  MAMMALIAN-CELL-CYCLE                                    19     1     51
004  ERBB-RECEPTOR-SIGNALING                                225    22   1100
005  FA-BRCA-PATHWAY                                         28     0    123
...
```

# Get a specific model

```bash
# Get rules for model 7
bnet models 7
```

prints:

```
targets,factors
v_Coup_fti, (!(v_Fgf8 | v_Sp8) | !(v_Sp8 | v_Fgf8))
v_Emx2, (v_Coup_fti & !((v_Fgf8 | v_Sp8) | v_Pax6))
v_Fgf8, ((v_Fgf8 & v_Sp8) & !v_Emx2)
v_Pax6, (v_Sp8 & !(v_Emx2 | v_Coup_fti))
v_Sp8, (v_Fgf8 & !v_Emx2)
```

```bash
# Get SBML for model 7
bnet models 7 -f booleannet
```

## Visualize a model


## Convert BBMB to JSON

Convert the BBMB model repository directory to a single JSON file. 

Skips a few large models that make the file too large.

```bash
python booleannet/bbm2json.py \
       --summary ~/src/biodivine-boolean-models/models/summary.csv 
       --models ~/src/biodivine-boolean-models/models 
       --skip 253,248,79,261,256
       --output models.json.gz
```

## Convert rules to images
