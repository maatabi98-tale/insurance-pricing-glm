***

# src/glm_engine.py

```python
"""
Actuarial GLM Pricing Engine.
Executes Poisson and Gamma regressions for frequency-severity modeling.
"""

import os
import logging
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats.contingency import association
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PricingGLMEngine:
    """
    Object-oriented architecture for calibrating insurance pure premium models.
    """

    def __init__(self, freq_data_path: str, sev_data_path: str):
        self.df_freq = self._load_data(freq_data_path)
        self.df_sev = self._load_data(sev_data_path)
        self.model_freq: Optional[sm.genmod.GeneralizedLinearResultsWrapper] = None
        self.model_sev: Optional[sm.genmod.GeneralizedLinearResultsWrapper] = None

    @staticmethod
    def _load_data(path: str) -> pd.DataFrame:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing dataset at {path}.")
        df = pd.read_csv(path)
        logging.info(f"Dataset ingested: {path} | Matrix shape: {df.shape}")
        return df

    def compute_cramers_v(self, feature1: str, feature2: str) -> float:
        """
        Evaluates Cramer's V statistic to detect structural multicollinearity 
        between categorical covariates.
        """
        contingency_matrix = pd.crosstab(self.df_freq[feature1], self.df_freq[feature2])
        v_stat = association(contingency_matrix, method="cramer")
        logging.info(f"Cramer's V ({feature1} vs {feature2}): {v_stat:.4f}")
        return v_stat

    def fit_frequency_model(self, formula: str, exposure_col: str) -> None:
        """
        Calibrates the Poisson GLM with a log-link function.
        Enforces exposure normalization via logarithmic offset.
        """
        logging.info(f"Initializing Poisson regression: {formula}")
        
        # Isolate strictly positive exposure
        df_fit = self.df_freq[self.df_freq[exposure_col] > 0].copy()
        offset_vector = np.log(df_fit[exposure_col])
        
        model = smf.glm(formula=formula, 
                        data=df_fit, 
                        offset=offset_vector,
                        family=sm.families.Poisson(link=sm.families.links.Log()))
        
        self.model_freq = model.fit()
        logging.info(f"Frequency Model Converged. Deviance: {self.model_freq.deviance:.2f}, AIC: {self.model_freq.aic:.2f}")

    def fit_severity_model(self, formula: str) -> None:
        """
        Calibrates the Gamma GLM with a log-link function.
        Restricted to strictly positive claim amounts.
        """
        logging.info(f"Initializing Gamma regression: {formula}")
        
        target_var = formula.split('~')[0].strip()
        df_fit = self.df_sev[self.df_sev[target_var] > 0].copy()
        
        model = smf.glm(formula=formula, 
                        data=df_fit,
                        family=sm.families.Gamma(link=sm.families.links.Log()))
        
        self.model_sev = model.fit()
        logging.info(f"Severity Model Converged. Deviance: {self.model_sev.deviance:.2f}, AIC: {self.model_sev.aic:.2f}")

    def export_parameters(self, freq_out: str, sev_out: str) -> None:
        """
        Extracts and writes parameter vectors (betas) and p-values to disk.
        """
        os.makedirs(os.path.dirname(freq_out), exist_ok=True)
        
        if self.model_freq:
            freq_res = pd.DataFrame({'Beta': self.model_freq.params, 'P_Value': self.model_freq.pvalues})
            freq_res.to_csv(freq_out)
            
        if self.model_sev:
            sev_res = pd.DataFrame({'Beta': self.model_sev.params, 'P_Value': self.model_sev.pvalues})
            sev_res.to_csv(sev_out)
            
        logging.info("Parameter vectors successfully exported to processed directory.")


if __name__ == "__main__":
    engine = PricingGLMEngine(freq_data_path="data/raw/base_freq.csv",
                              sev_data_path="data/raw/base_cout.csv")
    
    # Multicollinearity diagnostic step
    engine.compute_cramers_v('age_cl', 'anc_perm_cl')
    
    # Model specifications
    f_freq = "ns_bg ~ age_cl + anveh_cl + franchise + Formule + C(zone_bg)"
    f_sev = "cs_bg ~ age_cl + anveh_cl + franchise + Formule + C(zone_bg)"
    
    # Execution
    engine.fit_frequency_model(formula=f_freq, exposure_col="RA")
    engine.fit_severity_model(formula=f_sev)
    
    # Serialization
    engine.export_parameters("data/processed/beta_freq.csv", "data/processed/beta_sev.csv")
