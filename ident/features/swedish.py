"""
Swedish-specific feature extraction for text analysis.
"""

import re
from collections import Counter


class SwedishFeatures:
    """Extract Swedish-specific features from text."""

    # Common Swedish function words
    SWEDISH_FUNCTION_WORDS = {
        'och', 'i', 'att', 'det', 'som', 'en', 'på', 'är', 'för', 'av',
        'till', 'med', 'han', 'den', 'de', 'har', 'inte', 'var', 'ett', 'om',
        'så', 'men', 'kan', 'vi', 'ska', 'från', 'hon', 'dig', 'nu', 'sin',
        'dem', 'ut', 'än', 'då', 'än', 'hur', 'bara', 'sig', 'här', 'skulle',
    }

    # Common Swedish particles and adverbs
    SWEDISH_PARTICLES = {
        'ju', 'väl', 'nog', 'då', 'alltså', 'kanske', 'visst', 'faktiskt',
        'egentligen', 'förstås', 'naturligtvis', 'självklart',
    }

    # Swedish common prefixes
    SWEDISH_PREFIXES = {
        'för', 'be', 'an', 'av', 'å', 'bi', 'dis', 'er', 'för', 'ge',
        'miss', 'o', 'sam', 'und', 'van', 'zu',
    }

    # Swedish common suffixes
    SWEDISH_SUFFIXES = {
        'het', 'skap', 'dom', 'else', 'are', 'ande', 'ende', 'ing',
        'ning', 'ling', 'bar', 'lig', 'lös', 'sam', 'aktig',
    }

    @staticmethod
    def extract(text, words, sentences):
        """
        Extract Swedish-specific features from text.

        Args:
            text: Original text string
            words: List of words
            sentences: List of sentences

        Returns:
            Dictionary of Swedish-specific features
        """
        features = {}

        if not text or not words:
            return {
                'swedish_char_frequency': 0.0,
                'aa_frequency': 0.0,
                'ae_frequency': 0.0,
                'oe_frequency': 0.0,
                'compound_word_ratio': 0.0,
                'function_word_ratio': 0.0,
                'particle_frequency': 0.0,
                'avg_word_complexity': 0.0,
            }

        char_count = len(text)
        word_count = len(words)

        # Swedish character frequencies (å, ä, ö)
        aa_count = text.lower().count('å')
        ae_count = text.lower().count('ä')
        oe_count = text.lower().count('ö')

        features['aa_frequency'] = aa_count / char_count if char_count > 0 else 0.0
        features['ae_frequency'] = ae_count / char_count if char_count > 0 else 0.0
        features['oe_frequency'] = oe_count / char_count if char_count > 0 else 0.0

        # Combined Swedish character frequency
        swedish_chars = aa_count + ae_count + oe_count
        features['swedish_char_frequency'] = swedish_chars / char_count if char_count > 0 else 0.0

        # Compound word detection (words with 12+ characters likely compound)
        long_words = [w for w in words if len(w) >= 12]
        features['compound_word_ratio'] = len(long_words) / word_count if word_count > 0 else 0.0

        # Function word frequency
        words_lower = [w.lower() for w in words]
        function_word_count = sum(1 for w in words_lower if w in SwedishFeatures.SWEDISH_FUNCTION_WORDS)
        features['function_word_ratio'] = function_word_count / word_count if word_count > 0 else 0.0

        # Particle frequency
        particle_count = sum(1 for w in words_lower if w in SwedishFeatures.SWEDISH_PARTICLES)
        features['particle_frequency'] = particle_count / word_count if word_count > 0 else 0.0

        # Average word complexity (based on prefixes, suffixes, length)
        complexity_scores = []
        for word in words:
            if len(word) < 3:
                complexity_scores.append(0.0)
                continue

            score = 0.0
            word_lower = word.lower()

            # Length contributes to complexity
            score += min(len(word) / 15.0, 1.0)

            # Check for common prefixes
            for prefix in SwedishFeatures.SWEDISH_PREFIXES:
                if word_lower.startswith(prefix):
                    score += 0.2
                    break

            # Check for common suffixes
            for suffix in SwedishFeatures.SWEDISH_SUFFIXES:
                if word_lower.endswith(suffix):
                    score += 0.2
                    break

            # Swedish characters add complexity
            if any(c in word_lower for c in 'åäö'):
                score += 0.1

            complexity_scores.append(min(score, 1.0))

        features['avg_word_complexity'] = sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0.0

        # Double consonant frequency (common in Swedish)
        double_consonants = len(re.findall(r'([bcdfghjklmnpqrstvwxz])\1', text.lower(), re.UNICODE))
        features['double_consonant_frequency'] = double_consonants / char_count if char_count > 0 else 0.0

        # Swedish definite article usage (words ending in -en, -et, -n, -t, -na, -a)
        definite_patterns = [r'\w+en\b', r'\w+et\b', r'\w+na\b', r'\w+a\b']
        definite_count = sum(len(re.findall(pattern, text, re.UNICODE | re.IGNORECASE)) for pattern in definite_patterns)
        features['definite_article_ratio'] = definite_count / word_count if word_count > 0 else 0.0

        # Swedish verb patterns (infinitive -a ending)
        infinitive_verbs = len(re.findall(r'\b\w{3,}a\b', text, re.UNICODE))
        features['infinitive_verb_ratio'] = infinitive_verbs / word_count if word_count > 0 else 0.0

        return features
