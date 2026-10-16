# AGENTS.md — evals

What "good" means, as numbers with thresholds. Where the quality of an output is the product,
quality gets a subsystem rather than a script.

## What lives here

`EVAL-NNNN` definitions: the question each one answers, its dataset, its metrics and its
threshold. Datasets and runners live alongside them as they are built. None exist yet.

## The rules that make these trustworthy

- **Agreement with a model is not correctness.** Model-against-model scores are reported,
  never gated on. Every quality claim needs an independent label or a calibrated judge.
- **Slice by customer or segment.** A change that lifts the average and hurts one customer is a
  regression for that customer, and ships as one unless someone looks.
- **Pin the model and the prompt version**, or the run is not reproducible.
- **Datasets are versioned.** A score is comparable only against the same version.
- **Regression cases are permanent.** A case added because of a defect is never removed.

## When these run

A fast slice on every pull request that changes something an eval measures. The full suite
nightly and before any release.

## Working here

Adding or changing an eval is a quality change in itself. Say in the changelog what moved,
and re-baseline deliberately rather than as a side effect.
