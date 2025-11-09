"""
Main text style analyzer.
"""

import re
from typing import List, Optional
from ident.profile import TextProfile
from ident.features.lexical import LexicalFeatures
from ident.features.syntactic import SyntacticFeatures
from ident.features.character import CharacterFeatures
from ident.features.swedish import SwedishFeatures
from ident.features.stylometric import StylometricFeatures


class StyleAnalyzer:
    """
    Main analyzer for Swedish text style analysis.

    This class orchestrates the extraction of multiple feature types
    to create comprehensive text style profiles.
    """

    def __init__(self, min_words: int = 50):
        """
        Initialize the StyleAnalyzer.

        Args:
            min_words: Minimum number of words required for analysis (default: 50)
        """
        self.min_words = min_words

        # Initialize feature extractors
        self.lexical_extractor = LexicalFeatures()
        self.syntactic_extractor = SyntacticFeatures()
        self.character_extractor = CharacterFeatures()
        self.swedish_extractor = SwedishFeatures()
        self.stylometric_extractor = StylometricFeatures()

    def analyze(self, text: str, name: str = "Text") -> TextProfile:
        """
        Analyze text and create a style profile.

        Args:
            text: The text to analyze (Swedish text recommended, 400+ words)
            name: Name/identifier for this text

        Returns:
            TextProfile object containing all extracted features

        Raises:
            ValueError: If text is too short or empty
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Preprocess text
        words, sentences = self._preprocess_text(text)

        if len(words) < self.min_words:
            print(f"Warning: Text has only {len(words)} words. "
                  f"At least {self.min_words} words recommended for robust analysis. "
                  f"Results may be less reliable.")

        # Extract all features
        features = {}

        # Lexical features
        lexical_features = self.lexical_extractor.extract(text, words, sentences)
        features.update(lexical_features)

        # Syntactic features
        syntactic_features = self.syntactic_extractor.extract(text, words, sentences)
        features.update(syntactic_features)

        # Character features
        character_features = self.character_extractor.extract(text, words, sentences)
        features.update(character_features)

        # Swedish-specific features
        swedish_features = self.swedish_extractor.extract(text, words, sentences)
        features.update(swedish_features)

        # Stylometric features
        stylometric_features = self.stylometric_extractor.extract(text, words, sentences)
        features.update(stylometric_features)

        # Create and return profile
        profile = TextProfile(
            name=name,
            features=features,
            text_length=len(text)
        )

        return profile

    def analyze_multiple(self, texts: List[str], names: Optional[List[str]] = None) -> List[TextProfile]:
        """
        Analyze multiple texts and create profiles for each.

        Args:
            texts: List of texts to analyze
            names: Optional list of names for the texts

        Returns:
            List of TextProfile objects
        """
        if names is None:
            names = [f"Text {i+1}" for i in range(len(texts))]

        if len(names) != len(texts):
            raise ValueError("Number of names must match number of texts")

        profiles = []
        for text, name in zip(texts, names):
            try:
                profile = self.analyze(text, name)
                profiles.append(profile)
            except ValueError as e:
                print(f"Error analyzing '{name}': {e}")

        return profiles

    def _preprocess_text(self, text: str) -> tuple:
        """
        Preprocess text into words and sentences.

        Args:
            text: Raw text string

        Returns:
            Tuple of (words, sentences)
        """
        # Split into sentences (basic approach)
        # This handles common Swedish sentence delimiters
        sentence_endings = r'[.!?]+[\s\n]+'
        sentences = [s.strip() for s in re.split(sentence_endings, text) if s.strip()]

        # If no sentences found, treat entire text as one sentence
        if not sentences:
            sentences = [text.strip()]

        # Extract words (alphanumeric sequences)
        # This preserves Swedish characters (å, ä, ö)
        words = re.findall(r'\b\w+\b', text, re.UNICODE)

        return words, sentences

    def compare_profiles(self, profile1: TextProfile, profile2: TextProfile,
                        method: str = 'cosine') -> float:
        """
        Compare two text profiles.

        Args:
            profile1: First TextProfile
            profile2: Second TextProfile
            method: Comparison method ('cosine', 'euclidean', 'manhattan')

        Returns:
            Similarity score
        """
        return profile1.compare(profile2, method=method)

    def get_feature_names(self) -> List[str]:
        """
        Get list of all feature names that can be extracted.

        Returns:
            List of feature names
        """
        # Create a dummy analysis to get all feature names
        dummy_text = "Detta är en test text. " * 20
        try:
            profile = self.analyze(dummy_text, name="dummy")
            return sorted(profile.features.keys())
        except:
            return []

    def __repr__(self):
        return f"StyleAnalyzer(min_words={self.min_words})"
