# IDent - Swedish Text Style Analyzer

A comprehensive Python library for analyzing and comparing Swedish text writing styles. IDent extracts 30+ stylometric and linguistic features to create unique profiles for texts, enabling author identification, style comparison, and text analysis.

## Features

- **79+ Text Signals**: Comprehensive analysis including:
  - Lexical features (vocabulary richness, word lengths, etc.)
  - Syntactic features (sentence structure, punctuation patterns)
  - Character-level analysis (character distributions, Swedish character usage)
  - Stylometric features (type-token ratio, hapax legomena, Yule's K)
  - Swedish-specific features (compound words, Swedish character frequency)
  - **NEW: AI-detection features** (em dashes, transition words, sentence patterns, passive voice, etc.)

- **Style Profiling**: Create detailed profiles of writing styles from texts (400+ words recommended)

- **Comparison & Similarity**: Compare text profiles using multiple distance metrics

- **2D Visualization**: Generate PCA and t-SNE plots to visualize style differences

- **Simple API**: Easy-to-use interface for quick analysis

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from ident import StyleAnalyzer

# Initialize analyzer
analyzer = StyleAnalyzer()

# Analyze Swedish text
text1 = """Your Swedish text here (400+ words recommended)..."""
profile1 = analyzer.analyze(text1, name="Text 1")

text2 = """Another Swedish text..."""
profile2 = analyzer.analyze(text2, name="Text 2")

# Compare profiles
similarity = profile1.compare(profile2)
print(f"Similarity: {similarity:.2%}")

# Visualize multiple profiles
from ident.visualizer import visualize_profiles_2d

profiles = [profile1, profile2]
visualize_profiles_2d(profiles, method='pca', save_path='comparison.png')
```

## Detailed Usage

### Analyzing a Single Text

```python
from ident import StyleAnalyzer

analyzer = StyleAnalyzer()
profile = analyzer.analyze(text, name="My Text")

# Access features
print(f"Average word length: {profile.features['avg_word_length']:.2f}")
print(f"Vocabulary richness: {profile.features['type_token_ratio']:.3f}")
print(f"Average sentence length: {profile.features['avg_sentence_length']:.2f}")

# Get full feature report
profile.print_report()
```

### Comparing Multiple Texts

```python
from ident import StyleAnalyzer
from ident.comparator import compare_multiple_profiles

analyzer = StyleAnalyzer()

# Analyze multiple texts
profiles = []
for text, name in zip(texts, names):
    profile = analyzer.analyze(text, name=name)
    profiles.append(profile)

# Get similarity matrix
similarity_matrix = compare_multiple_profiles(profiles)
print(similarity_matrix)
```

### Visualization

```python
from ident.visualizer import visualize_profiles_2d, plot_feature_comparison

# 2D visualization with PCA
visualize_profiles_2d(profiles, method='pca', title='Text Style Comparison')

# 2D visualization with t-SNE
visualize_profiles_2d(profiles, method='tsne', perplexity=5)

# Compare specific features
plot_feature_comparison(profiles, features=['avg_word_length', 'type_token_ratio'])
```

## Features Analyzed

### Lexical Features
- Average word length
- Vocabulary richness (Type-Token Ratio)
- Lexical diversity (MTLD)
- Hapax legomena ratio
- Long word ratio (7+ characters)
- Short word ratio (1-3 characters)

### Syntactic Features
- Average sentence length
- Sentence length variance
- Punctuation frequency
- Question mark usage
- Exclamation mark usage
- Comma density

### Character-Level Features
- Character frequency distribution
- Swedish character usage (å, ä, ö)
- Digit ratio
- Uppercase ratio
- Whitespace patterns

### Stylometric Features
- Yule's K measure
- Simpson's D
- Honoré's R
- Function word frequency
- Content word ratio

### Swedish-Specific Features
- Compound word detection
- Swedish particle usage
- Nordic character density
- Swedish-specific punctuation patterns

## Requirements

- Python 3.7+
- numpy
- scipy
- scikit-learn
- matplotlib
- pandas

## Examples

See the `examples/` directory for complete usage examples:
- `basic_analysis.py` - Simple text analysis
- `compare_authors.py` - Compare multiple authors
- `visualize_styles.py` - Create 2D visualizations

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## Author

Created for robust Swedish text style analysis and author identification.
