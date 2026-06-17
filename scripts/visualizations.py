"""
Visualization module for extracted GLM parameter vectors.
Translates log-odds (betas) into multiplicative relativities.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'figure.dpi': 300
})

def plot_tariff_relativities(csv_path: str, title: str, output_path: str) -> None:
    """
    Ingests structural parameters, exponentiates them to extract relativities, 
    and plots the distribution against the baseline.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Parameter file missing: {csv_path}")

    df = pd.read_csv(csv_path, index_col=0)
    
    # Filter out Intercept for pure relativity analysis
    df = df[df.index != 'Intercept'].copy()
    
    # Compute multiplicative effect
    df['Relativity'] = np.exp(df['Beta'])
    df = df.sort_values(by='Relativity', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(x=df['Relativity'], y=df.index, ax=ax, palette='mako')
    
    # Baseline reference
    ax.axvline(1.0, color='#c0392b', linestyle='--', linewidth=1.5, label='Baseline (1.0)')
    
    ax.set_title(title, pad=15)
    ax.set_xlabel(r'Multiplicative Relativity ($\exp(\hat{\beta})$)')
    ax.set_ylabel('Risk Factor Modalities')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    plot_tariff_relativities("../data/processed/beta_freq.csv", 
                             "Frequency Model Relativities (Poisson)", 
                             "../data/processed/plot_freq_relativities.png")
    
    plot_tariff_relativities("../data/processed/beta_sev.csv", 
                             "Severity Model Relativities (Gamma)", 
                             "../data/processed/plot_sev_relativities.png")
