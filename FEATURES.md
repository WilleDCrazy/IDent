# IDent - Complete Feature List

## Overview

IDent extracts **89+ features** from Swedish texts for comprehensive style analysis, including advanced AI-detection features.

## Feature Categories

### 1. Lexical Features (19 features)

Analyze vocabulary and word usage patterns:

1. `total_words` - Total word count
2. `unique_words` - Number of unique words
3. `avg_word_length` - Average word length in characters
4. `word_length_variance` - Variance in word lengths
5. `type_token_ratio` - Vocabulary richness (unique/total)
6. `lexical_density` - Lexical diversity measure
7. `mtld` - Measure of Textual Lexical Diversity
8. `hapax_legomena_ratio` - Words appearing once
9. `hapax_dislegomena_ratio` - Words appearing twice
10. `long_word_ratio` - Ratio of 7+ character words
11. `short_word_ratio` - Ratio of 1-3 character words
12. `very_long_word_ratio` - Ratio of 10+ character words
13. `avg_chars_per_word` - Average characters per word
14. `avg_word_frequency` - Average word frequency
15. `avg_word_complexity` - Morphological complexity
16. `function_word_ratio` - Swedish function word usage
17. `compound_word_ratio` - Estimated compound words
18. `hapax_ratio` - Alternative hapax measure
19. `word_frequency_variance` - Variance in word frequencies

### 2. Syntactic Features (13 features)

Analyze sentence structure and punctuation:

1. `total_sentences` - Number of sentences
2. `avg_sentence_length` - Average sentence length in words
3. `sentence_length_variance` - Variance in sentence lengths
4. `punctuation_frequency` - Overall punctuation density
5. `comma_frequency` - Comma usage rate
6. `period_frequency` - Period usage rate
7. `question_mark_frequency` - Question mark usage
8. `exclamation_mark_frequency` - Exclamation mark usage
9. `semicolon_frequency` - Semicolon usage
10. `colon_frequency` - Colon usage
11. `comma_density` - Commas per sentence
12. `quote_frequency` - Quotation mark usage
13. `parentheses_frequency` - Parentheses usage
14. `dash_frequency` - Dash usage

### 3. Character Features (19 features)

Analyze character-level patterns:

1. `total_characters` - Total character count
2. `alphabetic_ratio` - Ratio of alphabetic characters
3. `digit_ratio` - Ratio of digit characters
4. `whitespace_ratio` - Ratio of whitespace
5. `uppercase_ratio` - Ratio of uppercase letters
6. `lowercase_ratio` - Ratio of lowercase letters
7. `special_char_ratio` - Ratio of special characters
8. `avg_chars_per_word` - Average characters per word
9. `vowel_ratio` - Vowel frequency (Swedish vowels)
10. `consonant_ratio` - Consonant frequency
11. `char_freq_1` through `char_freq_10` - Top 10 character frequencies

### 4. Swedish-Specific Features (11 features)

Features optimized for Swedish text:

1. `swedish_char_frequency` - Combined å, ä, ö frequency
2. `aa_frequency` - Frequency of å
3. `ae_frequency` - Frequency of ä
4. `oe_frequency` - Frequency of ö
5. `compound_word_ratio` - Swedish compound word detection
6. `function_word_ratio` - Swedish function words (och, att, som, etc.)
7. `particle_frequency` - Swedish particles (ju, väl, nog, etc.)
8. `avg_word_complexity` - Swedish morphological complexity
9. `double_consonant_frequency` - Double consonant patterns
10. `definite_article_ratio` - Definite article patterns (-en, -et, -na)
11. `infinitive_verb_ratio` - Infinitive verb patterns (-a ending)

### 5. Stylometric Features (10 features)

Advanced statistical measures:

1. `yules_k` - Yule's K measure (vocabulary richness)
2. `simpsons_d` - Simpson's D (diversity index)
3. `honores_r` - Honoré's R (vocabulary richness)
4. `sichels_s` - Sichel's S measure
5. `entropy` - Shannon entropy (text randomness)
6. `hapax_ratio` - Hapax legomena ratio
7. `dis_legomena_ratio` - Dis legomena ratio
8. `avg_word_frequency` - Average word frequency
9. `word_frequency_variance` - Variance in word frequencies
10. `burstiness` - Burstiness measure (word usage patterns)

### 6. AI-Detection Features (22 features)

Features commonly associated with AI-generated text:

**Basic AI Patterns:**
1. `em_dashes_per_sentence` - Em dash usage per sentence (AI tends to overuse)
2. `em_dash_frequency` - Overall em dash frequency in text
3. `lines_per_sentence` - Average lines/paragraphs per sentence
4. `newline_frequency` - Newline characters per sentence
5. `transition_word_frequency` - Transition word usage per sentence (however, moreover, etc.)
6. `transition_word_ratio` - Ratio of transition words to total words
7. `sentence_starter_diversity` - Variety in sentence opening words
8. `sentence_starter_repetition` - Repetition of most common sentence starter
9. `passive_voice_frequency` - Passive voice constructions per sentence
10. `adverb_frequency` - Qualifying adverb usage per sentence (particularly, significantly, etc.)
11. `adverb_ratio` - Ratio of qualifying adverbs to total words
12. `sentence_length_uniformity` - Coefficient of variation in sentence lengths (lower = more uniform)
13. `complex_punctuation_frequency` - Complex punctuation patterns (e.g., "...!", "?!")
14. `parenthetical_per_sentence` - Parenthetical expressions per sentence

**NEW: Sentence-Level Variability (Human text has MORE variability):**
15. `avg_punct_types_per_sentence` - Average number of different punctuation types per sentence
16. `punct_diversity_variance` - Variance in punctuation diversity across sentences
17. `avg_word_length_var_per_sentence` - Average word length variability within each sentence
18. `sentence_rhythm_variability` - Frequency of significant rhythm changes between sentences
19. `consecutive_sentence_similarity` - Similarity in length between consecutive sentences (AI higher)
20. `punctuation_variance_per_sentence` - Variability in punctuation counts across sentences
21. `consecutive_lexical_overlap` - Word overlap between consecutive sentences (AI higher)
22. `sentence_complexity_variance` - Variance in sentence complexity across text

## Usage Examples

### Accessing Features

```python
from ident import StyleAnalyzer

analyzer = StyleAnalyzer()
profile = analyzer.analyze(swedish_text, name="My Text")

# Access any feature
word_count = profile.features['total_words']
vocab_richness = profile.features['type_token_ratio']
swedish_chars = profile.features['swedish_char_frequency']

# Get all feature names
feature_names = sorted(profile.features.keys())
print(f"Total features: {len(feature_names)}")
```

### Comparing Specific Features

```python
# Focus on specific features for comparison
key_features = [
    'avg_word_length',
    'type_token_ratio',
    'avg_sentence_length',
    'yules_k',
    'swedish_char_frequency'
]

for feature in key_features:
    val1 = profile1.features[feature]
    val2 = profile2.features[feature]
    print(f"{feature}: {val1:.3f} vs {val2:.3f}")
```

### Feature Visualization

```python
from ident.visualizer import plot_feature_comparison

# Visualize specific features
plot_feature_comparison(
    profiles,
    features=['avg_word_length', 'type_token_ratio', 'mtld'],
    save_path='feature_comparison.png'
)
```

## Feature Interpretation

### Vocabulary Richness
- **type_token_ratio**: Higher = more varied vocabulary (0.5-0.9 typical)
- **mtld**: Higher = more diverse vocabulary (50-300 typical)
- **yules_k**: Lower = more diverse vocabulary (0-200 typical)

### Text Complexity
- **avg_word_length**: Longer words = more formal/technical (4-8 chars typical)
- **avg_sentence_length**: Longer sentences = more complex (10-25 words typical)
- **long_word_ratio**: Higher = more complex vocabulary (0.2-0.5 typical)

### Swedish Characteristics
- **swedish_char_frequency**: Higher = more distinctly Swedish (0.02-0.08 typical)
- **function_word_ratio**: Higher = more natural Swedish (0.2-0.4 typical)
- **compound_word_ratio**: Higher = more complex Swedish (0.1-0.3 typical)

### Writing Style
- **sentence_length_variance**: Higher = more varied writing style
- **punctuation_frequency**: Higher = more complex punctuation usage
- **entropy**: Higher = more unpredictable/creative text

### AI Detection Indicators
- **em_dashes_per_sentence**: AI text often uses more em dashes (>0.1 may indicate AI)
- **transition_word_frequency**: Higher frequency suggests AI-like writing (>0.3 typical for AI)
- **sentence_starter_diversity**: Lower diversity suggests repetitive AI patterns (0.7-0.9 typical for humans)
- **sentence_length_uniformity**: Lower values indicate more uniform AI-like structure (0.3-0.5 for AI, 0.6-1.0 for humans)
- **passive_voice_frequency**: Higher values may indicate AI formality (>0.5 suggests AI tendencies)
- **adverb_frequency**: High qualifying adverb usage is AI characteristic (>0.2 per sentence)

## Robustness

IDent is designed to be robust across different text types:

- **News articles**: Formal, balanced features
- **Blog posts**: Informal, higher particle usage
- **Academic texts**: High complexity, technical vocabulary
- **Fiction**: Varied sentence structure, creative language

Recommended minimum: **400+ words** for reliable profiling

## Feature Stability

Features are normalized and stable across different text lengths, making comparisons reliable and meaningful.
