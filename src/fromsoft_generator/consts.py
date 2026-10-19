"""
Gradient and colour constants.
"""

import csv
from pathlib import Path

GRADIENTS = {
    # fmt: off
    "gay":      "f00 f80 fe0 0a0 26c a0a",
    "trans":    "7bf 7bf f9a f9a fff fff f9a f9a 7bf 7bf",
    "bi":       "f08 f08 a6a 80f 80f",
    "lesbian":  "f20 f64 fa8 fff f8f f4c f08",
    "nb":       "ff2 fff 84d 333",
    "pan":      "f2c f2c ff2 ff2 2cf 2cf",
    "mlm":      "2a6 6ea 8fc fff 88f 44c 22a",
    "ace":      "000 aaa fff 808",
    "aro":      "000 aaa fff ad7 3a4",
    "aroace":   "235 6ad fff ec0 e80",
    "intersex": "70a 70a fd0 70a 70a",
    # fmt: on
}

MAPPING = dict(GRADIENTS)

with (Path(__file__).parent / "colors.tsv").open() as f:
    reader = csv.reader(f, delimiter="\t")
    for name, col in reader:
        MAPPING[name] = col
