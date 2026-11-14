"""
MONSOON PULSE — Statistical Analysis Engine Package
"""
from .mann_kendall import mann_kendall_test
from .theil_sen import theil_sen_estimator
from .autocorrelation import assess_autocorrelation
from .fdr_correction import benjamini_hochberg_correction
from .sensitivity_tester import SensitivityTester

__all__ = [
    "mann_kendall_test",
    "theil_sen_estimator",
    "assess_autocorrelation",
    "benjamini_hochberg_correction",
    "SensitivityTester",
]
