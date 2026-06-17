"""
Actuarial GLM Pricing Module.
Provides modular components for frequency-severity structural parameterization
and multicollinearity diagnostics.
"""

from .diagnostics import MulticollinearityAnalyzer
from .glm_pricing import PricingGLMEngine

__version__ = "1.0.0"
__author__ = "Quantitative Research Team"
