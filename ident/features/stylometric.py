"""
Stylometric feature extraction for text analysis.
"""

import math
from collections import Counter


class StylometricFeatures:
    """Extract stylometric features from text."""

    @staticmethod
    def extract(text, words, sentences):
        """
        Extract stylometric features from text.

        Args:
            text: Original text string
            words: List of words
            sentences: List of sentences

        Returns:
            Dictionary of stylometric features
        """
        features = {}

        if not words:
            return {
                'yules_k': 0.0,
                'simpsons_d': 0.0,
                'honores_r': 0.0,
                'sichels_s': 0.0,
                'entropy': 0.0,
            }

        word_count = len(words)
        word_freq = Counter(words)
        unique_words = len(word_freq)

        # Yule's K - measures vocabulary richness
        # K = 10000 * (M2 - M1) / (M1 * M1)
        # where M1 = number of words, M2 = sum of (freq^2) for each word type
        M1 = word_count
        M2 = sum(freq ** 2 for freq in word_freq.values())

        if M1 > 0:
            yules_k = 10000 * (M2 - M1) / (M1 * M1)
            features['yules_k'] = yules_k
        else:
            features['yules_k'] = 0.0

        # Simpson's D - measure of diversity
        # D = sum(n(n-1)) / (N(N-1))
        # where n = frequency of each word, N = total words
        if word_count > 1:
            simpsons_d = sum(freq * (freq - 1) for freq in word_freq.values()) / (word_count * (word_count - 1))
            features['simpsons_d'] = simpsons_d
        else:
            features['simpsons_d'] = 0.0

        # Honoré's R - vocabulary richness
        # R = 100 * log(N) / (1 - V1/V)
        # where N = total words, V = unique words, V1 = hapax legomena
        hapax = sum(1 for freq in word_freq.values() if freq == 1)
        if unique_words > 0 and hapax < unique_words:
            try:
                honores_r = 100 * math.log(word_count) / (1 - hapax / unique_words)
                features['honores_r'] = honores_r
            except (ValueError, ZeroDivisionError):
                features['honores_r'] = 0.0
        else:
            features['honores_r'] = 0.0

        # Sichel's S - measure of vocabulary richness
        # S = V2 / V (number of words occurring twice / total unique words)
        dis_legomena = sum(1 for freq in word_freq.values() if freq == 2)
        features['sichels_s'] = dis_legomena / unique_words if unique_words > 0 else 0.0

        # Shannon entropy - measure of randomness/diversity
        # H = -sum(p * log2(p)) where p = probability of each word
        entropy = 0.0
        for freq in word_freq.values():
            p = freq / word_count
            if p > 0:
                entropy -= p * math.log2(p)
        features['entropy'] = entropy

        # Frequency spectrum analysis
        freq_spectrum = Counter(word_freq.values())

        # Ratio of words appearing exactly once
        features['hapax_ratio'] = freq_spectrum.get(1, 0) / unique_words if unique_words > 0 else 0.0

        # Ratio of words appearing exactly twice
        features['dis_legomena_ratio'] = freq_spectrum.get(2, 0) / unique_words if unique_words > 0 else 0.0

        # Average word frequency
        features['avg_word_frequency'] = word_count / unique_words if unique_words > 0 else 0.0

        # Burstiness - measure of how bursty word usage is
        # Based on variance in word frequencies
        if unique_words > 1:
            mean_freq = word_count / unique_words
            freq_variance = sum((freq - mean_freq) ** 2 for freq in word_freq.values()) / unique_words
            features['word_frequency_variance'] = freq_variance
            features['burstiness'] = (math.sqrt(freq_variance) - mean_freq) / (math.sqrt(freq_variance) + mean_freq) if (math.sqrt(freq_variance) + mean_freq) > 0 else 0.0
        else:
            features['word_frequency_variance'] = 0.0
            features['burstiness'] = 0.0

        return features
