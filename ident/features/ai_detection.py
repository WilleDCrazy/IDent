"""
AI-detection feature extraction for text analysis.

This module extracts features commonly associated with AI-generated text,
which can be useful for detecting patterns typical of large language models.
"""

import re
from collections import Counter


class AIDetectionFeatures:
    """Extract AI-detection features from text."""

    # Common transition words that AI tends to overuse
    TRANSITION_WORDS = {
        # English transitions (for mixed texts)
        'however', 'moreover', 'furthermore', 'nevertheless', 'therefore',
        'consequently', 'additionally', 'meanwhile', 'subsequently',
        'nonetheless', 'thus', 'hence', 'accordingly', 'thereby',
        # Swedish transitions
        'dock', 'dessutom', 'däremot', 'emellertid', 'följaktligen',
        'således', 'därför', 'därtill', 'likväl', 'sålunda', 'vidare',
        'å andra sidan', 'å ena sidan', 'i kontrast', 'å sin sida'
    }

    # Common adverbs that AI tends to use frequently
    COMMON_ADVERBS = {
        # English adverbs
        'remarkably', 'particularly', 'significantly', 'notably', 'essentially',
        'fundamentally', 'primarily', 'specifically', 'generally', 'typically',
        'especially', 'effectively', 'efficiently', 'ultimately', 'consistently',
        'substantially', 'considerably', 'increasingly', 'critically', 'distinctly',
        # Swedish adverbs
        'anmärkningsvärt', 'särskilt', 'avsevärt', 'noterbart', 'väsentligen',
        'grundläggande', 'främst', 'specifikt', 'generellt', 'typiskt',
        'speciellt', 'effektivt', 'i slutändan', 'konsekvent', 'betydligt',
        'avsevärt', 'allt mer', 'kritiskt', 'tydligt', 'märkbart'
    }

    # Passive voice indicators (Swedish and English)
    PASSIVE_INDICATORS = {
        # Swedish passive forms
        r'\b\w+s\b',  # Swedish s-passive (e.g., "används", "kallas")
        r'\bblir?\s+\w+(ad|t|de|tt)\b',  # blir + participle
        r'\b(har|hade)\s+blivit\s+\w+(ad|t|de|tt)\b',  # har/hade blivit + participle
        # English passive forms
        r'\b(is|are|was|were|been|be|being)\s+\w+ed\b',
        r'\b(is|are|was|were|been|be|being)\s+\w+en\b'
    }

    @staticmethod
    def extract(text, words, sentences):
        """
        Extract AI-detection features from text.

        Args:
            text: Original text string
            words: List of words
            sentences: List of sentences

        Returns:
            Dictionary of AI-detection features
        """
        features = {}

        if not sentences or not words:
            return {
                'em_dashes_per_sentence': 0.0,
                'em_dash_frequency': 0.0,
                'lines_per_sentence': 0.0,
                'newline_frequency': 0.0,
                'transition_word_frequency': 0.0,
                'transition_word_ratio': 0.0,
                'sentence_starter_diversity': 0.0,
                'sentence_starter_repetition': 0.0,
                'passive_voice_frequency': 0.0,
                'adverb_frequency': 0.0,
                'adverb_ratio': 0.0,
                'sentence_length_uniformity': 0.0,
            }

        sentence_count = len(sentences)
        word_count = len(words)
        char_count = len(text)

        # Feature 1: Em dashes per sentence (AI tends to overuse em dashes)
        em_dashes = text.count('—') + text.count('--')  # Both em dash and double hyphen
        features['em_dashes_per_sentence'] = em_dashes / sentence_count if sentence_count > 0 else 0.0
        features['em_dash_frequency'] = em_dashes / char_count if char_count > 0 else 0.0

        # Feature 2: Lines per sentence (newlines can indicate structure)
        # Count explicit newlines
        newlines = text.count('\n')
        features['lines_per_sentence'] = (newlines + 1) / sentence_count if sentence_count > 0 else 1.0
        features['newline_frequency'] = newlines / sentence_count if sentence_count > 0 else 0.0

        # Feature 3: Transition word frequency (AI overuses transitions)
        text_lower = text.lower()
        transition_count = sum(
            len(re.findall(r'\b' + re.escape(word) + r'\b', text_lower))
            for word in AIDetectionFeatures.TRANSITION_WORDS
        )
        features['transition_word_frequency'] = transition_count / sentence_count if sentence_count > 0 else 0.0
        features['transition_word_ratio'] = transition_count / word_count if word_count > 0 else 0.0

        # Feature 4: Sentence starter diversity (AI tends to have repetitive starters)
        sentence_starters = []
        for sent in sentences:
            # Get first 1-2 words of each sentence
            sent_words = re.findall(r'\b\w+\b', sent, re.UNICODE)
            if sent_words:
                # Use first word or first two words
                if len(sent_words) >= 2:
                    starter = f"{sent_words[0].lower()} {sent_words[1].lower()}"
                else:
                    starter = sent_words[0].lower()
                sentence_starters.append(starter)

        if sentence_starters:
            unique_starters = len(set(sentence_starters))
            features['sentence_starter_diversity'] = unique_starters / len(sentence_starters)

            # Calculate repetition score (most common starter frequency)
            starter_counts = Counter(sentence_starters)
            most_common_freq = starter_counts.most_common(1)[0][1] if starter_counts else 0
            features['sentence_starter_repetition'] = most_common_freq / len(sentence_starters)
        else:
            features['sentence_starter_diversity'] = 0.0
            features['sentence_starter_repetition'] = 0.0

        # Feature 5: Passive voice frequency (AI sometimes overuses passive voice)
        passive_count = 0
        for pattern in AIDetectionFeatures.PASSIVE_INDICATORS:
            passive_count += len(re.findall(pattern, text, re.IGNORECASE))

        features['passive_voice_frequency'] = passive_count / sentence_count if sentence_count > 0 else 0.0

        # Feature 6: Adverb frequency (AI tends to use more qualifying adverbs)
        adverb_count = sum(
            1 for word in words
            if word.lower() in AIDetectionFeatures.COMMON_ADVERBS
        )
        features['adverb_frequency'] = adverb_count / sentence_count if sentence_count > 0 else 0.0
        features['adverb_ratio'] = adverb_count / word_count if word_count > 0 else 0.0

        # Feature 7: Sentence length uniformity (AI text often has more uniform sentence lengths)
        # Calculate coefficient of variation for sentence lengths
        sentence_lengths = []
        for sent in sentences:
            sent_words = re.findall(r'\b\w+\b', sent, re.UNICODE)
            sentence_lengths.append(len(sent_words))

        if sentence_lengths and len(sentence_lengths) > 1:
            mean_length = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((length - mean_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
            std_dev = variance ** 0.5
            # Coefficient of variation (lower = more uniform)
            features['sentence_length_uniformity'] = std_dev / mean_length if mean_length > 0 else 0.0
        else:
            features['sentence_length_uniformity'] = 0.0

        # Feature 8: Complex punctuation patterns (multiple punctuation types together)
        # AI sometimes uses patterns like "...!", "?!", etc.
        complex_punct = len(re.findall(r'[.!?]{2,}|[.!?][.!?]+', text))
        features['complex_punctuation_frequency'] = complex_punct / sentence_count if sentence_count > 0 else 0.0

        # Feature 9: Parenthetical expressions per sentence (AI uses these for clarification)
        parentheticals = text.count('(') + text.count('[')
        features['parenthetical_per_sentence'] = parentheticals / sentence_count if sentence_count > 0 else 0.0

        return features
