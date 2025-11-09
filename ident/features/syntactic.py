"""
Syntactic feature extraction for text analysis.
"""

import re
from collections import Counter


class SyntacticFeatures:
    """Extract syntactic features from text."""

    @staticmethod
    def extract(text, words, sentences):
        """
        Extract syntactic features from text.

        Args:
            text: Original text string
            words: List of words
            sentences: List of sentences

        Returns:
            Dictionary of syntactic features
        """
        features = {}

        if not sentences:
            return {
                'avg_sentence_length': 0.0,
                'sentence_length_variance': 0.0,
                'total_sentences': 0,
                'punctuation_frequency': 0.0,
                'comma_frequency': 0.0,
                'period_frequency': 0.0,
                'question_mark_frequency': 0.0,
                'exclamation_mark_frequency': 0.0,
                'semicolon_frequency': 0.0,
                'colon_frequency': 0.0,
                'comma_density': 0.0,
            }

        sentence_count = len(sentences)
        features['total_sentences'] = sentence_count

        # Sentence lengths in words
        sentence_lengths = []
        for sent in sentences:
            sent_words = re.findall(r'\b\w+\b', sent, re.UNICODE)
            sentence_lengths.append(len(sent_words))

        if sentence_lengths:
            features['avg_sentence_length'] = sum(sentence_lengths) / len(sentence_lengths)

            # Sentence length variance
            mean_length = features['avg_sentence_length']
            variance = sum((length - mean_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
            features['sentence_length_variance'] = variance
        else:
            features['avg_sentence_length'] = 0.0
            features['sentence_length_variance'] = 0.0

        # Punctuation analysis
        char_count = len(text)

        punctuation_counts = {
            ',': text.count(','),
            '.': text.count('.'),
            '?': text.count('?'),
            '!': text.count('!'),
            ';': text.count(';'),
            ':': text.count(':'),
        }

        total_punctuation = sum(punctuation_counts.values())

        features['punctuation_frequency'] = total_punctuation / char_count if char_count > 0 else 0.0
        features['comma_frequency'] = punctuation_counts[','] / char_count if char_count > 0 else 0.0
        features['period_frequency'] = punctuation_counts['.'] / char_count if char_count > 0 else 0.0
        features['question_mark_frequency'] = punctuation_counts['?'] / char_count if char_count > 0 else 0.0
        features['exclamation_mark_frequency'] = punctuation_counts['!'] / char_count if char_count > 0 else 0.0
        features['semicolon_frequency'] = punctuation_counts[';'] / char_count if char_count > 0 else 0.0
        features['colon_frequency'] = punctuation_counts[':'] / char_count if char_count > 0 else 0.0

        # Comma density (commas per sentence)
        features['comma_density'] = punctuation_counts[','] / sentence_count if sentence_count > 0 else 0.0

        # Quotation usage
        features['quote_frequency'] = (text.count('"') + text.count("'")) / char_count if char_count > 0 else 0.0

        # Parentheses usage
        features['parentheses_frequency'] = (text.count('(') + text.count(')')) / char_count if char_count > 0 else 0.0

        # Dash usage
        features['dash_frequency'] = (text.count('-') + text.count('–') + text.count('—')) / char_count if char_count > 0 else 0.0

        return features
