# mushroom-modeling

Exploration and modeling of a mushroom classification dataset toward a goal of
determining the features that make 'good soup'.

**Educational only: this is not mushroom identification, foraging, or food-safety
advice. Do not use these notebooks, dataset labels, odor categories, or rules to
decide whether to pick, cook, or eat a mushroom.** "Good soup" is the project's
playful framing, not a validated measure of taste or safety. The original notebook
commentary is preserved as exploratory thinking, not endorsed biological or
food-safety guidance.

## Start here

Read [rule_mining_mushrooms.ipynb](rule_mining_mushrooms.ipynb) first for the
odor-based "good soup" question and association rules, then
[mushroom_clustering.ipynb](mushroom_clustering.ipynb) for a separate clustering
exploration. Each notebook loads its own data; neither depends on the other.
You can inspect the saved outputs on GitHub without running Python.

The educational questions are: which recorded features co-occur with an
odor-derived "good" label, and how do mushrooms group by their recorded
categorical features? Neither notebook establishes real-world edibility.

## What the notebooks actually do

| Notebook | Methods |
| --- | --- |
| [Rule mining](rule_mining_mushrooms.ipynb) | Converts columns to categories, drops `veil-type`, and fills missing `stalk-root` values with `Unknown`. Maps odor codes `a` (almond) and `l` (anise) to `good`, `n` (none) to `neutral`, and all others to `rotten`, renaming this target `good_for_soup`. Explores correlations of factorized categories and decision-tree feature importance. One-hot encodes features selected by absolute correlation greater than 0.15, then uses Apriori with minimum support 0.07 and association rules with lift at least 1. Filters to confidence greater than 0.6 and consequent `good_for_soup_good`, sorting by confidence and lift. |
| [Clustering](mushroom_clustering.ipynb) | Separates the `class` label, one-hot encodes and standardizes the remaining features, and uses PCA retaining 99% of variance. Explores Ward hierarchical clustering and K-means, including an inertia sweep over 1-19 clusters and knee detection, then an eight-cluster fit. Plots clusters against class and odor. Fits logistic regression to cluster labels and searches `C` with five-fold cross-validation. |

## Dataset and attribution

Both notebooks now load the official
[UCI raw data](https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data)
for the [Mushroom dataset](https://archive.ics.uci.edu/dataset/73/mushroom).
Dataset attribution: Mushroom [Dataset], UCI Machine Learning Repository (1987),
DOI [10.24432/C5959T](https://doi.org/10.24432/C5959T), licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
This attribution and license describe the dataset, separately from this
repository's analysis. The UCI page defines the categorical letter codes.

The raw file is headerless and class-first: 8,124 records, 22 categorical
attributes plus `class` (`e`: 4,208; `p`: 3,916). Both loaders supply explicit
column names and `header=None`, parse the 2,480 `?` stalk-root markers as missing
with `na_values=['?']`, then restore the historical feature-first, class-last
column order. The `bruises` name is supplied directly, rather than renamed from
the old DataHub header `bruises%3F`. Existing categorical conversion and
`Unknown` filling remain in place.

No full dataset snapshot, checksum, or download date is committed. The exact original CSV
snapshot and its equivalence to any current UCI download have not been verified.
The original DataHub URL returned **HTTP 404** during the documentation check on
2026-10-24. The loader repair explicitly replaces that URL with UCI for future
runs. Saved `info()` outputs also show 8,124 rows and 2,480 missing stalk-root
values before filling, but matching counts do not prove snapshot equivalence.
All saved outputs, execution counts, and analyses remain historical and unchanged;
they were not regenerated with the repaired loaders.

## Saved results, not newly reproduced findings

These are observations from committed cell outputs, not a fresh execution:

| Location | Saved evidence | Interpretation limit |
| --- | --- | --- |
| Clustering: cell containing `kl.elbow` | Knee detector returns `8`. | Depends on preprocessing and unseeded K-means fits; not a biological taxonomy. |
| Clustering: cells containing `lr.score` and `fin_gs.best_score_` | Training score `1.0`; grid-search output `Best score: 1.000` and `C: 0.023299518105153717`. | `cluster_label` is included in `X_dummies` while predicting those same labels, leaking the target. These are not valid independent accuracy estimates. The later prose's 99.2% claim does not match these saved outputs. |
| Rule mining: cell containing `print(len(gfs_rules))` | Prints `420` rules after the stated filters. | Describes associations in the analyzed dataset, not tested taste or safety predictions. Execution counts are nonsequential, so saved outputs need not represent a single clean run. |

## Setup and reproduction status

The notebooks record a Python **3.8.10** kernel. There is no dependency lockfile
or tested environment specification. For a fresh exploratory environment, these
commands install the directly imported packages; they are **unverified starting
instructions**, not a guaranteed compatible environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install jupyterlab numpy pandas matplotlib seaborn scikit-learn scipy kneed mlxtend graphviz
.\.venv\Scripts\python.exe -m jupyterlab
```

The repaired loaders use the UCI endpoint above; loading the full dataset still
requires network access. A complete top-to-bottom run has not been validated.
The `graphviz` Python package is imported in
the rule-mining notebook, but the current cells do not render a Graphviz tree;
system Graphviz would be needed if that rendering were added.

Neither notebook was executed end to end for the loader repair. No new model
results or figures were generated. Current package versions may require API changes; Ward
linkage and Apriori can also be memory-intensive.

### Offline loader regression checks

The focused checks use Python's standard-library `unittest` runner and pandas
only; pytest, Jupyter, and the modeling packages are not required. With pandas
installed in the chosen environment, run from the repository root:

```powershell
python -m unittest discover -s tests -v
```

The tests redirect each notebook's CSV request to a three-row, illustrative
UCI-format fixture in `tests/fixtures/mushroom.data` (not a historical snapshot).
They execute only the loader cells and the isolated existing `stalk-root` fill
assignment: no data download, analysis/model cells, or notebook output writes.
They check first-row retention, all 23 field mappings, feature/class ordering,
categorical dtypes, `?` parsing, and `Unknown` filling without changing other
columns. These checks do not establish full-notebook reproducibility.

## Limitations and later work

- `good_for_soup` is an odor recoding, not a measured flavor or edibility outcome.
  The rule-mining predictors retain `class`, so some rules assume an
  edible/poisonous label is already known.
- Pearson correlations of arbitrary factorization codes are encoding-dependent.
  Feature selection and rule mining use the full dataset. Although a train/test
  split is created, the subsequent tree and rules do not evaluate on that
  held-out split.
- K-means and the decision tree have no fixed random seed. Clustering preprocesses
  the full dataset, and the logistic-regression target leakage prevents treating
  its scores as evidence of generalization.
- Cluster-to-genus/family interpretations in the original prose remain hypotheses;
  no taxonomic validation is provided. Dataset associations do not establish
  causation or applicability to mushrooms outside this dataset.

A later reproducibility pass can record a versioned snapshot and checksum,
document a tested dependency set, and rerun both notebooks from clean kernels.
Correcting leakage and adding meaningful held-out evaluation would be separate
analysis work; this loader repair preserves the original research and saved outputs.
