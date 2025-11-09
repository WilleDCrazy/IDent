"""
Character-level feature extraction for text analysis.
"""

import re
from collections import Counter


class CharacterFeatures:
    """Extract character-level features from text."""

    @staticmethod
    def extract(text, words, sentences):
        """
        Extract character-level features from text.

        Args:
            text: Original text string
            words: List of words
            sentences: List of sentences

        Returns:
            Dictionary of character-level features
        """
        features = {}

        if not text:
            return {
                'total_characters': 0,
                'alphabetic_ratio': 0.0,
                'digit_ratio': 0.0,
                'whitespace_ratio': 0.0,
                'uppercase_ratio': 0.0,
                'lowercase_ratio': 0.0,
                'special_char_ratio': 0.0,
                'avg_chars_per_word': 0.0,
            }

        char_count = len(text)
        features['total_characters'] = char_count

        # Character type ratios
        alphabetic = sum(1 for c in text if c.isalpha())
        digit = sum(1 for c in text if c.isdigit())
        whitespace = sum(1 for c in text if c.isspace())
        uppercase = sum(1 for c in text if c.isupper())
        lowercase = sum(1 for c in text if c.islower())

        features['alphabetic_ratio'] = alphabetic / char_count if char_count > 0 else 0.0
        features['digit_ratio'] = digit / char_count if char_count > 0 else 0.0
        features['whitespace_ratio'] = whitespace / char_count if char_count > 0 else 0.0
        features['uppercase_ratio'] = uppercase / alphabetic if alphabetic > 0 else 0.0
        features['lowercase_ratio'] = lowercase / alphabetic if alphabetic > 0 else 0.0

        # Special characters (not alphanumeric or whitespace)
        special = sum(1 for c in text if not c.isalnum() and not c.isspace())
        features['special_char_ratio'] = special / char_count if char_count > 0 else 0.0

        # Average characters per word
        if words:
            total_word_chars = sum(len(word) for word in words)
            features['avg_chars_per_word'] = total_word_chars / len(words)
        else:
            features['avg_chars_per_word'] = 0.0

        # Character frequency distribution (top 10 most common)
        char_freq = Counter(text.lower())
        # Remove whitespace from frequency analysis
        char_freq.pop(' ', None)
        char_freq.pop('\n', None)
        char_freq.pop('\t', None)

        # Get top character frequencies (normalized)
        if char_freq:
            most_common = char_freq.most_common(10)
            for i, (char, count) in enumerate(most_common):
                features[f'char_freq_{i+1}'] = count / char_count if char_count > 0 else 0.0

        # Vowel vs consonant ratio (for Swedish)
        swedish_vowels = set('aeiouyåäö')
        vowel_count = sum(1 for c in text.lower() if c in swedish_vowels)
        consonant_count = sum(1 for c in text.lower() if c.isalpha() and c not in swedish_vowels)

        features['vowel_ratio'] = vowel_count / alphabetic if alphabetic > 0 else 0.0
        features['consonant_ratio'] = consonant_count / alphabetic if alphabetic > 0 else 0.0

        return features
