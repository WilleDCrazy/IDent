"""
IDent - Swedish Text Style Analyzer
====================================

A comprehensive library for analyzing and comparing Swedish text writing styles.

Main components:
- StyleAnalyzer: Main analyzer class
- TextProfile: Text profile representation
- visualizer: Visualization functions
- comparator: Comparison and similarity metrics
"""

from ident.analyzer import StyleAnalyzer
from ident.profile import TextProfile

__version__ = "0.1.0"
__all__ = ["StyleAnalyzer", "TextProfile"]
