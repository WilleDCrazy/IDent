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

        # NEW FEATURES: Sentence-level variability analysis

        # Feature 10: Punctuation diversity per sentence (AI has less diverse punctuation)
        punctuation_per_sentence = []
        for sent in sentences:
            punct_types = set()
            for char in sent:
                if char in '.,!?;:—-()[]"\'':
                    punct_types.add(char)
            punctuation_per_sentence.append(len(punct_types))

        if punctuation_per_sentence:
            features['avg_punct_types_per_sentence'] = sum(punctuation_per_sentence) / len(punctuation_per_sentence)
            # Variability in punctuation diversity across sentences
            mean_punct = features['avg_punct_types_per_sentence']
            if mean_punct > 0:
                punct_variance = sum((p - mean_punct) ** 2 for p in punctuation_per_sentence) / len(punctuation_per_sentence)
                features['punct_diversity_variance'] = punct_variance ** 0.5
            else:
                features['punct_diversity_variance'] = 0.0
        else:
            features['avg_punct_types_per_sentence'] = 0.0
            features['punct_diversity_variance'] = 0.0

        # Feature 11: Word length variability PER sentence (AI more consistent within sentences)
        word_length_vars_per_sentence = []
        for sent in sentences:
            sent_words = re.findall(r'\b\w+\b', sent, re.UNICODE)
            if len(sent_words) > 1:
                lengths = [len(w) for w in sent_words]
                mean_len = sum(lengths) / len(lengths)
                var = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
                word_length_vars_per_sentence.append(var ** 0.5)
            else:
                word_length_vars_per_sentence.append(0.0)

        if word_length_vars_per_sentence:
            features['avg_word_length_var_per_sentence'] = sum(word_length_vars_per_sentence) / len(word_length_vars_per_sentence)
        else:
            features['avg_word_length_var_per_sentence'] = 0.0

        # Feature 12: Sentence rhythm patterns (consecutive short-long variations)
        # AI tends to have more predictable rhythm
        rhythm_changes = 0
        if len(sentence_lengths) > 1:
            for i in range(len(sentence_lengths) - 1):
                curr_len = sentence_lengths[i]
                next_len = sentence_lengths[i + 1]
                # Significant change if difference > 30% of mean
                if mean_length > 0 and abs(curr_len - next_len) > 0.3 * mean_length:
                    rhythm_changes += 1
            features['sentence_rhythm_variability'] = rhythm_changes / (len(sentence_lengths) - 1) if len(sentence_lengths) > 1 else 0.0
        else:
            features['sentence_rhythm_variability'] = 0.0

        # Feature 13: Consecutive sentence similarity (AI repeats structures)
        consecutive_similarities = []
        for i in range(len(sentence_lengths) - 1):
            curr_len = sentence_lengths[i]
            next_len = sentence_lengths[i + 1]
            # Normalized similarity (1 - normalized difference)
            max_len = max(curr_len, next_len, 1)
            similarity = 1.0 - abs(curr_len - next_len) / max_len
            consecutive_similarities.append(similarity)

        if consecutive_similarities:
            features['consecutive_sentence_similarity'] = sum(consecutive_similarities) / len(consecutive_similarities)
        else:
            features['consecutive_sentence_similarity'] = 0.0

        # Feature 14: Punctuation variance across sentences (AI more uniform punctuation)
        punct_counts_per_sentence = []
        for sent in sentences:
            punct_count = sum(1 for char in sent if char in '.,!?;:—-()[]"\'')
            punct_counts_per_sentence.append(punct_count)

        if punct_counts_per_sentence and len(punct_counts_per_sentence) > 1:
            mean_punct_count = sum(punct_counts_per_sentence) / len(punct_counts_per_sentence)
            if mean_punct_count > 0:
                punct_count_variance = sum((p - mean_punct_count) ** 2 for p in punct_counts_per_sentence) / len(punct_counts_per_sentence)
                features['punctuation_variance_per_sentence'] = (punct_count_variance ** 0.5) / mean_punct_count
            else:
                features['punctuation_variance_per_sentence'] = 0.0
        else:
            features['punctuation_variance_per_sentence'] = 0.0

        # Feature 15: Lexical repetition across consecutive sentences (AI repeats words)
        lexical_overlap_scores = []
        for i in range(len(sentences) - 1):
            curr_words = set(re.findall(r'\b\w+\b', sentences[i].lower(), re.UNICODE))
            next_words = set(re.findall(r'\b\w+\b', sentences[i + 1].lower(), re.UNICODE))
            if curr_words and next_words:
                overlap = len(curr_words & next_words) / len(curr_words | next_words)
                lexical_overlap_scores.append(overlap)

        if lexical_overlap_scores:
            features['consecutive_lexical_overlap'] = sum(lexical_overlap_scores) / len(lexical_overlap_scores)
        else:
            features['consecutive_lexical_overlap'] = 0.0

        # Feature 16: Sentence complexity variance (mix of simple and complex)
        # Measure by unique punctuation + word length in each sentence
        complexity_scores = []
        for sent in sentences:
            sent_words = re.findall(r'\b\w+\b', sent, re.UNICODE)
            if sent_words:
                avg_word_len = sum(len(w) for w in sent_words) / len(sent_words)
                punct_count = sum(1 for char in sent if char in ',;:—-()[]')
                complexity = avg_word_len + punct_count * 0.5  # Weight punctuation
                complexity_scores.append(complexity)

        if complexity_scores and len(complexity_scores) > 1:
            mean_complexity = sum(complexity_scores) / len(complexity_scores)
            if mean_complexity > 0:
                complexity_variance = sum((c - mean_complexity) ** 2 for c in complexity_scores) / len(complexity_scores)
                features['sentence_complexity_variance'] = (complexity_variance ** 0.5) / mean_complexity
            else:
                features['sentence_complexity_variance'] = 0.0
        else:
            features['sentence_complexity_variance'] = 0.0

        return features
