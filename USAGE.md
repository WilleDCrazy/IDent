# IDent Usage Guide

Complete guide to using the Swedish Text Style Analyzer.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Detailed Examples](#detailed-examples)
5. [Feature Reference](#feature-reference)
6. [Best Practices](#best-practices)

## Installation

```bash
# Clone the repository
git clone https://github.com/WilleDCrazy/IDent.git
cd IDent

# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

## Quick Start

### Basic Analysis

```python
from ident import StyleAnalyzer

analyzer = StyleAnalyzer()

text = """Your Swedish text here (400+ words recommended)..."""
profile = analyzer.analyze(text, name="My Text")

# Print report
profile.print_report()

# Access features
print(f"Word count: {profile.features['total_words']}")
print(f"Vocabulary richness: {profile.features['type_token_ratio']:.3f}")
```

### Comparing Two Texts

```python
text1 = """First Swedish text..."""
text2 = """Second Swedish text..."""

profile1 = analyzer.analyze(text1, name="Text 1")
profile2 = analyzer.analyze(text2, name="Text 2")

# Calculate similarity (0-1, higher = more similar)
similarity = profile1.compare(profile2, method='cosine')
print(f"Similarity: {similarity:.2%}")
```

### Visualizing Multiple Texts

```python
from ident.visualizer import visualize_profiles_2d

profiles = [profile1, profile2, profile3]

# Create PCA visualization
visualize_profiles_2d(profiles, method='pca', save_path='comparison.png')

# Create t-SNE visualization
visualize_profiles_2d(profiles, method='tsne', perplexity=5)
```

## Core Concepts

### TextProfile

A `TextProfile` object represents the stylistic fingerprint of a text. It contains:

- **name**: Identifier for the text
- **features**: Dictionary of extracted features (30+ metrics)
- **text_length**: Original text length in characters

```python
# Create a profile
profile = analyzer.analyze(text, name="Example")

# Access features
avg_word_length = profile.features['avg_word_length']
sentence_length = profile.features['avg_sentence_length']

# Export to JSON
profile.to_json('my_profile.json')

# Load from JSON
loaded_profile = TextProfile.from_json('my_profile.json')
```

### StyleAnalyzer

The main analysis engine that extracts features from text.

```python
# Initialize with custom settings
analyzer = StyleAnalyzer(min_words=50)

# Analyze single text
profile = analyzer.analyze(text, name="Text")

# Analyze multiple texts
profiles = analyzer.analyze_multiple(
    texts=[text1, text2, text3],
    names=["Text 1", "Text 2", "Text 3"]
)

# Get available feature names
features = analyzer.get_feature_names()
```

## Detailed Examples

### Finding Distinctive Features

```python
from ident.comparator import get_distinctive_features

distinctive = get_distinctive_features(profile1, profile2, top_n=10)

for feature, (val1, val2, diff) in distinctive.items():
    print(f"{feature}:")
    print(f"  Text 1: {val1:.4f}")
    print(f"  Text 2: {val2:.4f}")
    print(f"  Difference: {diff:.4f}\n")
```

### Creating Comparison Matrix

```python
from ident.comparator import compare_multiple_profiles

similarity_matrix = compare_multiple_profiles(profiles, method='cosine')
print(similarity_matrix)

# Export to CSV
similarity_matrix.to_csv('similarity.csv')
```

### Finding Most Similar Texts

```python
from ident.comparator import find_most_similar

# Find 5 most similar texts to a reference
similar = find_most_similar(
    profile=reference_profile,
    candidates=all_profiles,
    method='cosine',
    top_n=5
)

for profile, similarity in similar:
    print(f"{profile.name}: {similarity:.3f}")
```

### Clustering Texts

```python
from ident.comparator import cluster_profiles

clusters = cluster_profiles(profiles, n_clusters=3, method='kmeans')

for cluster_id, cluster_profiles in clusters.items():
    print(f"Cluster {cluster_id}:")
    for profile in cluster_profiles:
        print(f"  - {profile.name}")
```

### Advanced Visualization

```python
from ident.visualizer import (
    plot_feature_comparison,
    plot_similarity_heatmap,
    plot_radar_chart
)

# Compare specific features
plot_feature_comparison(
    profiles,
    features=['avg_word_length', 'type_token_ratio', 'yules_k'],
    save_path='features.png'
)

# Similarity heatmap
plot_similarity_heatmap(
    profiles,
    method='cosine',
    save_path='heatmap.png'
)

# Radar chart
plot_radar_chart(
    profiles,
    top_n=8,
    save_path='radar.png'
)
```

## Feature Reference

### Lexical Features (11 features)
- `avg_word_length`: Average word length in characters
- `type_token_ratio`: Unique words / total words (vocabulary richness)
- `mtld`: Measure of Textual Lexical Diversity
- `hapax_legomena_ratio`: Ratio of words appearing once
- `hapax_dislegomena_ratio`: Ratio of words appearing twice
- `long_word_ratio`: Ratio of words with 7+ characters
- `short_word_ratio`: Ratio of words with 1-3 characters
- `very_long_word_ratio`: Ratio of words with 10+ characters
- `unique_words`: Number of unique words
- `total_words`: Total word count
- `lexical_density`: Unique words / total words

### Syntactic Features (13 features)
- `avg_sentence_length`: Average sentence length in words
- `sentence_length_variance`: Variance in sentence lengths
- `total_sentences`: Number of sentences
- `punctuation_frequency`: Overall punctuation density
- `comma_frequency`: Comma usage frequency
- `period_frequency`: Period usage frequency
- `question_mark_frequency`: Question mark usage
- `exclamation_mark_frequency`: Exclamation mark usage
- `semicolon_frequency`: Semicolon usage
- `colon_frequency`: Colon usage
- `comma_density`: Commas per sentence
- `quote_frequency`: Quotation mark usage
- `parentheses_frequency`: Parentheses usage

### Character Features (17+ features)
- `total_characters`: Total character count
- `alphabetic_ratio`: Ratio of alphabetic characters
- `digit_ratio`: Ratio of digit characters
- `whitespace_ratio`: Ratio of whitespace
- `uppercase_ratio`: Ratio of uppercase letters
- `lowercase_ratio`: Ratio of lowercase letters
- `special_char_ratio`: Ratio of special characters
- `avg_chars_per_word`: Average characters per word
- `vowel_ratio`: Vowel frequency (Swedish vowels: a,e,i,o,u,y,å,ä,ö)
- `consonant_ratio`: Consonant frequency
- `char_freq_1` to `char_freq_10`: Top 10 character frequencies

### Swedish-Specific Features (9 features)
- `swedish_char_frequency`: Combined frequency of å, ä, ö
- `aa_frequency`: Frequency of å
- `ae_frequency`: Frequency of ä
- `oe_frequency`: Frequency of ö
- `compound_word_ratio`: Estimated compound word frequency
- `function_word_ratio`: Swedish function word usage
- `particle_frequency`: Swedish particle usage (ju, väl, nog, etc.)
- `avg_word_complexity`: Average morphological complexity
- `double_consonant_frequency`: Double consonant patterns
- `definite_article_ratio`: Definite article endings (-en, -et, etc.)
- `infinitive_verb_ratio`: Infinitive verb patterns (-a ending)

### Stylometric Features (10 features)
- `yules_k`: Yule's K measure (vocabulary richness)
- `simpsons_d`: Simpson's D (diversity index)
- `honores_r`: Honoré's R (vocabulary richness)
- `sichels_s`: Sichel's S measure
- `entropy`: Shannon entropy (text randomness)
- `hapax_ratio`: Hapax legomena ratio
- `dis_legomena_ratio`: Dis legomena ratio
- `avg_word_frequency`: Average word frequency
- `word_frequency_variance`: Variance in word frequencies
- `burstiness`: Burstiness measure (word usage patterns)

**Total: 60+ features extracted**

## Best Practices

### Text Length

- **Minimum**: 50 words (will show warning)
- **Recommended**: 400+ words for robust analysis
- **Optimal**: 1000+ words for highly accurate profiling

### Comparison Methods

**Cosine Similarity** (recommended for style comparison)
- Range: 0 (completely different) to 1 (identical)
- Good for comparing overall style
- Insensitive to magnitude differences

**Euclidean Distance**
- Range: 0 (identical) to infinity
- Lower values = more similar
- Sensitive to feature magnitudes

**Manhattan Distance**
- Range: 0 (identical) to infinity
- Lower values = more similar
- Less sensitive to outliers than Euclidean

### Visualization Tips

**PCA (Principal Component Analysis)**
- Best for: Initial exploration, linear relationships
- Works well with: Any number of profiles
- Preserves: Global structure

**t-SNE (t-Distributed Stochastic Neighbor Embedding)**
- Best for: Complex relationships, clusters
- Requires: 5+ profiles for good results
- Preserves: Local structure
- Adjust `perplexity`: Use 1/3 of number of profiles

### Performance Tips

1. **Batch Processing**: Use `analyze_multiple()` instead of loops
2. **Feature Selection**: Focus on relevant features for your use case
3. **Caching**: Save profiles to JSON and reuse them
4. **Normalization**: Features are automatically normalized for comparison

### Common Use Cases

**Author Identification**
```python
# Analyze known author samples
known_profiles = analyzer.analyze_multiple(known_texts, known_names)

# Analyze unknown text
unknown_profile = analyzer.analyze(unknown_text, "Unknown")

# Find most similar
similar = find_most_similar(unknown_profile, known_profiles, top_n=3)
```

**Genre Classification**
```python
# Create genre centroids
news_centroid = calculate_profile_centroid(news_profiles)
blog_centroid = calculate_profile_centroid(blog_profiles)

# Compare new text to centroids
# ... implementation
```

**Text Quality Assessment**
```python
# Compare against high-quality reference texts
# Focus on lexical diversity, sentence structure
quality_indicators = [
    'mtld',
    'type_token_ratio',
    'avg_sentence_length',
    'sentence_length_variance'
]
```

## Troubleshooting

**Issue**: Warning about text length
- **Solution**: Provide texts with 400+ words for reliable results

**Issue**: Clustering fails
- **Solution**: Ensure you have enough profiles (>= n_clusters)

**Issue**: t-SNE produces poor results
- **Solution**: Adjust perplexity parameter or use PCA instead

**Issue**: Features seem unusual
- **Solution**: Check that text is actually Swedish; library optimized for Swedish

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/WilleDCrazy/IDent/issues
- Documentation: See README.md

## License

MIT License - See LICENSE file for details
