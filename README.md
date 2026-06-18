# Predictive Modeling for Insurance Pricing: GLM Frequency-Severity Architecture

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14%2B-green)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-lightgrey)

## Context and Objective
This repository deploys a quantitative actuarial pricing engine for a motor insurance guarantee (glass breakage). The architecture leverages empirical policyholder exposure and claims datasets to compute the theoretical pure premium using a decoupled frequency-severity framework.
It features a modern Python (Statsmodels) OOP refactoring of a legacy actuarial pricing engine originally developed in SAS. The original SAS PROC GENMOD routines and collinearity diagnostics are preserved in the legacy_sas/ directory for mathematical audit and equivalence verification.

## Mathematical Methodology
The pricing algorithm models claim counts and costs via independent Generalized Linear Models (GLM) belonging to the Exponential Dispersion Family (EDF):
*   **Frequency Model:** Assumes claim counts follow a Poisson distribution. The systematic component utilizes a logarithmic link function. To account for heterogeneous policy durations, the logarithm of the risk exposure ($RA$, Risques-Années) is strictly enforced as an offset variable.
*   **Severity Model:** Assumes strictly positive claim costs follow a Gamma distribution, characterized by a constant coefficient of variation. A logarithmic link function ensures non-negative cost predictions.
*   **Multicollinearity Diagnostics:** Cramer's V statistic is evaluated pairwise across the categorical feature space (e.g., driver age vs. license seniority) to isolate and eliminate linearly dependent covariates prior to structural calibration.
*   **Pure Premium:** Derived under the assumption of stochastic independence between frequency and severity: $\mathbb{E}[PP] = \mathbb{E}[Frequency] \times \mathbb{E}[Severity]$.

## Directory Architecture
```text
├── data/
│   ├── raw/                 # Ingestion point for base_freq.csv and base_cout.csv
│   └── processed/
├── legacy_sas/
│   ├── /          #original SAS code
├── src/
│   ├── __init__.py
│   └── glm_engine.py        # Core OOP GLM estimation and inference engine
├── scripts/
│   └── visualizations.py    # Analytical plotting for tariff relativities
├── requirements.txt
└── README.md
