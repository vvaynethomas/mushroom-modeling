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

Both notebooks request the same
[DataHub CSV](https://datahub.io/machine-learning/mushroom/r/mushroom.csv).
The dataset corresponds to the
[UCI Machine Learning Repository's Mushroom dataset](https://archive.ics.uci.edu/dataset/73/mushroom),
whose feature definitions explain the letter codes, including odor and the
missing stalk-root marker `?`. Attribute the dataset to that source, separately
from this repository's analysis.

Saved `info()` outputs in both notebooks show 8,124 rows and 23 columns: 22
categorical attributes plus the `class` label. They show 2,480 missing stalk-root
values before filling. The UCI schema uses `?` for missing stalk-root values;
these notebooks rely on the CSV exposing them as nulls. A replacement data source
must preserve or explicitly reconcile that behavior and the column names
(including the notebooks' `bruises%3F` rename).

No data file, checksum, or download date is committed. The exact original CSV
snapshot and its equivalence to any current UCI download have not been verified.
The original DataHub URL returned **HTTP 404** during the documentation check on
2026-10-24; no replacement source was silently substituted.

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

Open a notebook in that environment and run its cells from top to bottom only
after resolving the dataset URL. The `graphviz` Python package is imported in
the rule-mining notebook, but the current cells do not render a Graphviz tree;
system Graphviz would be needed if that rendering were added.

For this documentation pass, notebook JSON/schema validation and inspection of
code and saved outputs were performed, along with a request to the original
dataset URL. Neither notebook was executed end to end: the URL is unavailable
and the local interpreter lacks the analysis packages. No new model results or
figures were generated. Current package versions may require API changes; Ward
linkage and Apriori can also be memory-intensive.

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

A later reproducibility pass can establish a permitted, versioned data source,
document a tested dependency set, and rerun both notebooks from clean kernels.
Correcting leakage and adding meaningful held-out evaluation would be separate
analysis work; this first pass preserves the original research and saved outputs.
