"""
Feature extraction modules for text analysis.
"""

from ident.features.lexical import LexicalFeatures
from ident.features.syntactic import SyntacticFeatures
from ident.features.character import CharacterFeatures
from ident.features.swedish import SwedishFeatures
from ident.features.stylometric import StylometricFeatures

__all__ = [
    "LexicalFeatures",
    "SyntacticFeatures",
    "CharacterFeatures",
    "SwedishFeatures",
    "StylometricFeatures"
]
