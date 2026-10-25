"""Exercise only notebook loading and missing-value filling, using offline data."""

import ast
import contextlib
import csv
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "mushroom.data"
URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "mushroom/agaricus-lepiota.data"
)
FEATURES = [
    "cap-shape", "cap-surface", "cap-color", "bruises", "odor",
    "gill-attachment", "gill-spacing", "gill-size", "gill-color",
    "stalk-shape", "stalk-root", "stalk-surface-above-ring",
    "stalk-surface-below-ring", "stalk-color-above-ring",
    "stalk-color-below-ring", "veil-type", "veil-color", "ring-number",
    "ring-type", "spore-print-color", "population", "habitat",
]
NOTEBOOKS = [
    ("mushroom_clustering.ipynb", 2, 3, "df"),
    ("rule_mining_mushrooms.ipynb", 1, 3, "mushroom_df"),
]


class NotebookLoaderTests(unittest.TestCase):
    def load_notebook_data(self, filename, loader_index, variable):
        notebook = json.loads((ROOT / filename).read_text(encoding="utf-8"))
        namespace = {"pd": pd}
        read_csv = pd.read_csv

        def read_fixture(url, **kwargs):
            self.assertEqual(url, URL)
            self.assertIsNone(kwargs["header"])
            self.assertEqual(kwargs["names"], ["class"] + FEATURES)
            self.assertEqual(kwargs["na_values"], ["?"])
            return read_csv(FIXTURE, **kwargs)

        with patch.object(pd, "read_csv", side_effect=read_fixture) as reader:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(
                    "".join(notebook["cells"][loader_index]["source"]),
                    namespace,
                )
        reader.assert_called_once()
        return notebook, namespace, namespace[variable]

    def test_headerless_schema_and_categorical_missing_values(self):
        with FIXTURE.open(encoding="utf-8", newline="") as fixture:
            rows = list(csv.reader(fixture))
        for filename, loader, fill, variable in NOTEBOOKS:
            with self.subTest(notebook=filename):
                _, _, frame = self.load_notebook_data(
                    filename, loader, variable
                )
                self.assertEqual(frame.shape, (3, 23))
                self.assertEqual(list(frame.columns), FEATURES + ["class"])
                self.assertTrue(
                    all(isinstance(dtype, pd.CategoricalDtype) for dtype in frame.dtypes)
                )
                # Check every field, including the first record, against raw positions.
                for index, row in enumerate(rows):
                    for column, value in zip(["class"] + FEATURES, row):
                        actual = frame.loc[index, column]
                        if value == "?":
                            self.assertTrue(pd.isna(actual))
                        else:
                            self.assertEqual(actual, value)
                self.assertEqual(frame["class"].tolist(), ["p", "e", "e"])
                self.assertEqual(frame["stalk-root"].isna().sum(), 1)
                self.assertEqual(frame.isna().sum().sum(), 1)
                self.assertNotIn("?", frame["stalk-root"].cat.categories)

    def test_existing_unknown_fill_preserves_categories(self):
        for filename, loader, fill, variable in NOTEBOOKS:
            with self.subTest(notebook=filename):
                notebook, namespace, frame = self.load_notebook_data(
                    filename, loader, variable
                )
                before = frame.copy(deep=True)
                tree = ast.parse("".join(notebook["cells"][fill]["source"]))
                # Isolate the existing fill; do not execute odor recoding or analyses.
                assignments = []
                for node in tree.body:
                    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                        continue
                    target = node.targets[0]
                    if not (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == variable
                    ):
                        continue
                    key = target.slice
                    if isinstance(key, ast.Index):  # Python 3.8 wraps subscript keys.
                        key = key.value
                    if isinstance(key, ast.Constant) and key.value == "stalk-root":
                        assignments.append(node)
                self.assertEqual(len(assignments), 1)
                exec(
                    compile(
                        ast.Module(body=assignments, type_ignores=[]),
                        filename,
                        "exec",
                    ),
                    namespace,
                )
                result = namespace[variable]
                self.assertEqual(result["stalk-root"].tolist(), ["e", "c", "Unknown"])
                self.assertIsInstance(result["stalk-root"].dtype, pd.CategoricalDtype)
                self.assertEqual(
                    set(result["stalk-root"].cat.categories),
                    set(before["stalk-root"].cat.categories) | {"Unknown"},
                )
                self.assertFalse(result.isna().any().any())
                pd.testing.assert_frame_equal(
                    result.drop(columns="stalk-root"),
                    before.drop(columns="stalk-root"),
                )


if __name__ == "__main__":
    unittest.main()
