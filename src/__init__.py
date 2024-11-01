"""
Election Prediction Tool
-------------------
A Streamlit application for election outcome analysis using Monte Carlo simulation.

This package provides tools for:
- Simulating election outcomes
- Analyzing voter behavior
- Visualizing results
"""

from src import auth, simulation, visualization

__version__ = "0.1.0"
__author__ = "Strategy Ace LLC"
__license__ = "MIT"
__copyright__ = "Copyright 2024 Strategy Ace LLC"

# Define public API
__all__ = [
    'auth',
    'simulation',
    'visualization'
]
