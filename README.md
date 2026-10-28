# Mushroom modeling: patterns, clusters, and "good soup"

Explore mushroom descriptions from two angles: **which features occur together,
and which mushrooms group together?** These notebooks use the UCI Mushroom
dataset to turn categorical observations into association rules, visualizations,
and exploratory clusters.

**Educational only: do not use these notebooks to identify, forage, cook, or eat
mushrooms.**

## Explore the notebooks

Browse the saved charts and tables directly on GitHub, starting with either
notebook. Each loads its own data and can be explored independently.

| Notebook | Question and approach | Saved highlights |
| --- | --- | --- |
| [Rule mining](rule_mining_mushrooms.ipynb) | What feature combinations accompany an odor-derived "good soup" label? Correlation heatmaps and decision-tree feature importances lead into Apriori frequent-itemset mining and association rules. | **420 rules** meet the notebook's filters, including confidence greater than 0.6 for the `good_for_soup_good` consequent. |
| [Clustering](mushroom_clustering.ipynb) | How do mushrooms group by their recorded features? One-hot encoding, scaling, and PCA feed Ward hierarchical clustering and K-means; plots compare the groups with class and odor. | The saved inertia-curve knee is **eight clusters**, followed by an eight-cluster fit and class/odor visualizations. |

Association rules make combinations of categorical features easy to inspect.
**Support** measures how often both sides of a rule occur together;
**confidence** measures how often the consequent occurs among records matching
the antecedent; **lift** compares that confidence with the consequent's overall
frequency. Clustering offers a complementary view of similarity, without using
`class` to form the groups.

### Reading the results

"Good soup" is a playful odor proxy: almond and anise become `good`, no odor
becomes `neutral`, and other odor codes become `rotten`. The rules describe
full-dataset associations (some include the recorded `class` label), not measured
flavor. The later logistic-regression step includes its target cluster labels
among its inputs, so its scores are not independent predictive evidence.
The highlights above come from historical saved outputs, not a fresh run.

## Try it locally

Open either notebook in JupyterLab:

```powershell
git clone https://github.com/vvaynethomas/mushroom-modeling.git
cd mushroom-modeling
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install jupyterlab numpy pandas matplotlib seaborn scikit-learn scipy kneed mlxtend graphviz
.\.venv\Scripts\python.exe -m jupyterlab
```

These are starting instructions for exploration, not a tested environment:
the notebooks record Python 3.8.10, and current package APIs may differ.
Loading data requires internet access; Ward linkage and Apriori can be
memory-intensive. Work in a notebook copy to keep your experiments separate
from the saved examples.

The [loader checks](tests/test_notebook_loaders.py) run offline with pandas:

```powershell
python -m unittest discover -s tests -v
```

Further work is tracked in
[reproduction and environment setup](https://github.com/vvaynethomas/mushroom-modeling/issues/3)
and [evaluation design](https://github.com/vvaynethomas/mushroom-modeling/issues/4).

## Dataset and attribution

Both notebooks load the official
[UCI raw data](https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data).
The [Mushroom dataset page](https://archive.ics.uci.edu/dataset/73/mushroom)
explains the categorical feature codes.

Mushroom [Dataset], UCI Machine Learning Repository (1987),
DOI [10.24432/C5959T](https://doi.org/10.24432/C5959T).
The dataset is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/);
this attribution and license apply to the dataset, separately from this
repository's analysis.
