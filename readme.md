This repo contains code to construct sentiment data for African American Vernacular English (AAE) vs. Standard American English (SAE) from tweets.

The original TwitterAAE dataset is from [Blodgett et. al. (2016)](https://aclanthology.org/D16-1120/). While the original paper aimed to train a dialect-estimation model, once dialect has been estimated, the data can be used to study disparities in performance of AAVE vs. SAE for NLP tasks --- sentiment is one such task. Prior work that uses sentiment from TwitterAAE includes [Bagdasaryan et. al. (2019)](https://arxiv.org/pdf/1905.12101.pdf) and [Elazar et. al. (2018)](https://arxiv.org/pdf/1808.06640.pdf).

The heuristic to estimate sentiment is from Elazar et. al. and is fairly simple (even though the unicode wrestling to achieve it is not). If a tweet includes 🙂, 😈, 😆, 😅, 😂, 😀, 😺 etc., it's positive. If it includes 😡, 😤, 😰, 🤢, 👿 etc., it's negative. If both types of emojis occur, sentiment cannot be inferred. Appendix C in Elazar et. al. has the full emoji list.

Code in this repo is taken from Elazar et. al.'s [Github](https://github.com/yanaiela/demog-text-removal). I did the labor of running an extinct version of Python to re-create this dataset and share it.

### Data
- `data/raw/sentiment_race` contains full tweet texts, files for AAE and SAE are separate, files for positive ("happy") and negative ("sad") sentiments are separate.
- `data/processed/sentiment_race` contains the tokenized dataset (using `twokenize.py`). Each row contains token IDs corresponding to line number in`vocab`.

### How to re-generate data
First, build the conda environment to run this code. You will need vintage Python 2.7

```
CONDA_SUBDIR=osx-64  # this is for backwards compatibility with Apple silicon
conda create -f env_py27.yml
conda activate py27
```

If `conda create -f` doesn't work and you'd like to instantiate a new Python 2 environment, you can do so with `CONDA_SUBDIR=osx-64 conda create -n py27 python=2.7` and then `conda install --file env_py27.yml`.

- Download the original dataset (`TwitterAAE-full-v1.zip`) from http://slanglab.cs.umass.edu/TwitterAAE/ and unzip it
- Run `python make_data.py <path_to_unzipped_folder>/twitteraae_all raw/sentiment_race processed/sentiment_race sentiment race`. The parameters are: source data path, raw output path, tokenized output path, task type (sentiment), demographic type (race).

### Contributing
If anyone has the time to port this codebase and all its unicode regexes to Python 3, it would be a good thing to do --- happy to take PRs here.