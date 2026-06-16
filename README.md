# Glass Breakage Insurance Pricing: GLM Frequency-Severity Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14%2B-green)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-lightgrey)

## Context and Objective
This repository contains a quantitative pricing framework for a motor insurance glass breakage guarantee. The objective is to estimate the pure premium relying on empirical policyholder and claims datasets, utilizing a standard frequency-severity actuarial approach.

## Mathematical Methodology
The pricing engine models claim counts and claim costs independently using Generalized Linear Models (GLMs):
*   **Frequency Model:** Assumes claim counts follow a Poisson distribution. The systematic component utilizes a logarithmic link function, incorporating the logarithm of the risk-exposure (`log_RA`) as an offset variable to normalize heterogeneous policy durations.
*   **Severity Model:** Assumes strictly positive claim costs follow a Gamma distribution with a constant coefficient of variation. A logarithmic link function is applied to ensure strictly positive cost predictions.
*   **Collinearity Diagnostics:** Cramer's V statistic is computed pairwise among categorical covariates to detect structural multicollinearity prior to model fitting.
*   **Pure Premium:** Derived under the assumption of independence between frequency and severity as $\mathbb{E}[PP] = \mathbb{E}[Frequency] \times \mathbb{E}[Severity]$. 

## Project Architecture
```text
├── data/
│   ├── raw/                 # Raw policyholder (base_freq.csv) and claims (base_cout.csv) datasets
│   └── processed/           # Model outputs and coefficient tables
├── src/
│   ├── __init__.py
│   ├── glm_pricing.py       # Core OOP GLM estimation engine
│   └── diagnostics.py       # Statistical testing and Cramer's V logic
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
├── requirements.txt
└── README.md
