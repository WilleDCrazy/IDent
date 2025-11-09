"""
Lexical feature extraction for text analysis.
"""

import re
from collections import Counter
import math


class LexicalFeatures:
    """Extract lexical features from text."""

    @staticmethod
    def extract(text, words, sentences):
        """
        Extract lexical features from text.

        Args:
            text: Original text string
            words: List of words
            sentences: List of sentences

        Returns:
            Dictionary of lexical features
        """
        features = {}

        if not words:
            return {
                'avg_word_length': 0.0,
                'type_token_ratio': 0.0,
                'hapax_legomena_ratio': 0.0,
                'hapax_dislegomena_ratio': 0.0,
                'long_word_ratio': 0.0,
                'short_word_ratio': 0.0,
                'unique_words': 0,
                'total_words': 0,
                'lexical_density': 0.0,
                'word_length_variance': 0.0,
            }

        # Basic counts
        word_count = len(words)
        features['total_words'] = word_count

        # Word lengths
        word_lengths = [len(word) for word in words]
        features['avg_word_length'] = sum(word_lengths) / len(word_lengths)

        # Word length variance
        mean_length = features['avg_word_length']
        variance = sum((length - mean_length) ** 2 for length in word_lengths) / len(word_lengths)
        features['word_length_variance'] = variance

        # Vocabulary richness
        word_freq = Counter(words)
        unique_words = len(word_freq)
        features['unique_words'] = unique_words
        features['type_token_ratio'] = unique_words / word_count if word_count > 0 else 0.0

        # Hapax legomena (words appearing once)
        hapax_legomena = sum(1 for freq in word_freq.values() if freq == 1)
        features['hapax_legomena_ratio'] = hapax_legomena / word_count if word_count > 0 else 0.0

        # Hapax dislegomena (words appearing twice)
        hapax_dislegomena = sum(1 for freq in word_freq.values() if freq == 2)
        features['hapax_dislegomena_ratio'] = hapax_dislegomena / word_count if word_count > 0 else 0.0

        # Long words (7+ characters)
        long_words = sum(1 for length in word_lengths if length >= 7)
        features['long_word_ratio'] = long_words / word_count if word_count > 0 else 0.0

        # Short words (1-3 characters)
        short_words = sum(1 for length in word_lengths if 1 <= length <= 3)
        features['short_word_ratio'] = short_words / word_count if word_count > 0 else 0.0

        # Very long words (10+ characters)
        very_long_words = sum(1 for length in word_lengths if length >= 10)
        features['very_long_word_ratio'] = very_long_words / word_count if word_count > 0 else 0.0

        # Lexical density (unique words / total words)
        features['lexical_density'] = unique_words / word_count if word_count > 0 else 0.0

        # MTLD (Measure of Textual Lexical Diversity) - simplified version
        features['mtld'] = LexicalFeatures._calculate_mtld(words)

        return features

    @staticmethod
    def _calculate_mtld(words, threshold=0.72):
        """
        Calculate MTLD (Measure of Textual Lexical Diversity).

        This is a simplified version that measures the average number of words
        needed to maintain a certain type-token ratio.
        """
        if len(words) < 50:
            return 0.0

        def _mtld_calc(word_list):
            factor = 0
            factor_lengths = []
            types = set()
            tokens = 0

            for word in word_list:
                word_lower = word.lower()
                types.add(word_lower)
                tokens += 1

                if tokens > 0:
                    ttr = len(types) / tokens
                    if ttr < threshold:
                        factor += 1
                        factor_lengths.append(tokens)
                        types = set()
                        tokens = 0

            if tokens > 0:
                ttr = len(types) / tokens
                factor += (1.0 - ttr) / (1.0 - threshold)
                factor_lengths.append(tokens)

            if factor > 0:
                return len(word_list) / factor
            return 0.0

        # Calculate forward and backward
        forward = _mtld_calc(words)
        backward = _mtld_calc(words[::-1])

        if forward > 0 and backward > 0:
            return (forward + backward) / 2
        elif forward > 0:
            return forward
        elif backward > 0:
            return backward
        return 0.0
