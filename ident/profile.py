"""
Text profile representation and comparison.
"""

import numpy as np
from typing import Dict, List, Optional
import json


class TextProfile:
    """
    Represents a text style profile with extracted features.
    """

    def __init__(self, name: str, features: Dict[str, float], text_length: int = 0):
        """
        Initialize a text profile.

        Args:
            name: Name/identifier for this text
            features: Dictionary of extracted features
            text_length: Length of the original text in characters
        """
        self.name = name
        self.features = features
        self.text_length = text_length
        self._feature_vector = None

    def get_feature_vector(self, feature_names: Optional[List[str]] = None) -> np.ndarray:
        """
        Get features as a numpy array.

        Args:
            feature_names: List of feature names to include (if None, use all)

        Returns:
            Numpy array of feature values
        """
        if feature_names is None:
            feature_names = sorted(self.features.keys())

        vector = np.array([self.features.get(name, 0.0) for name in feature_names])
        return vector

    def compare(self, other: 'TextProfile', method: str = 'cosine') -> float:
        """
        Compare this profile with another profile.

        Args:
            other: Another TextProfile to compare with
            method: Comparison method ('cosine', 'euclidean', 'manhattan')

        Returns:
            Similarity score (higher = more similar for cosine, lower = more similar for distance metrics)
        """
        # Get common features
        common_features = sorted(set(self.features.keys()) & set(other.features.keys()))

        if not common_features:
            return 0.0

        # Get feature vectors
        vec1 = self.get_feature_vector(common_features)
        vec2 = other.get_feature_vector(common_features)

        if method == 'cosine':
            # Cosine similarity (0 to 1, higher is more similar)
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            return dot_product / (norm1 * norm2)

        elif method == 'euclidean':
            # Euclidean distance (lower is more similar)
            return np.linalg.norm(vec1 - vec2)

        elif method == 'manhattan':
            # Manhattan distance (lower is more similar)
            return np.sum(np.abs(vec1 - vec2))

        else:
            raise ValueError(f"Unknown comparison method: {method}")

    def print_report(self, top_n: int = 20):
        """
        Print a formatted report of the profile features.

        Args:
            top_n: Number of top features to display
        """
        print(f"\n{'='*60}")
        print(f"Text Style Profile: {self.name}")
        print(f"{'='*60}")
        print(f"Text length: {self.text_length} characters\n")

        # Group features by category
        categories = {
            'Lexical': [],
            'Syntactic': [],
            'Character': [],
            'Swedish': [],
            'Stylometric': [],
            'Other': []
        }

        for feature_name, value in self.features.items():
            # Categorize based on feature name
            if any(keyword in feature_name for keyword in ['word', 'lexical', 'hapax', 'token', 'mtld']):
                categories['Lexical'].append((feature_name, value))
            elif any(keyword in feature_name for keyword in ['sentence', 'punctuation', 'comma', 'period']):
                categories['Syntactic'].append((feature_name, value))
            elif any(keyword in feature_name for keyword in ['char', 'uppercase', 'lowercase', 'digit', 'vowel', 'consonant']):
                categories['Character'].append((feature_name, value))
            elif any(keyword in feature_name for keyword in ['swedish', 'aa_', 'ae_', 'oe_', 'function_word', 'particle']):
                categories['Swedish'].append((feature_name, value))
            elif any(keyword in feature_name for keyword in ['yules', 'simpsons', 'honores', 'sichels', 'entropy', 'burstiness']):
                categories['Stylometric'].append((feature_name, value))
            else:
                categories['Other'].append((feature_name, value))

        # Print features by category
        for category, features in categories.items():
            if features:
                print(f"\n{category} Features:")
                print(f"{'-'*60}")
                for feature_name, value in sorted(features, key=lambda x: -abs(x[1]))[:top_n]:
                    # Format feature name
                    display_name = feature_name.replace('_', ' ').title()
                    print(f"  {display_name:.<45} {value:>10.4f}")

        print(f"\n{'='*60}\n")

    def to_dict(self) -> dict:
        """
        Convert profile to dictionary.

        Returns:
            Dictionary representation of the profile
        """
        return {
            'name': self.name,
            'text_length': self.text_length,
            'features': self.features
        }

    def to_json(self, filepath: str):
        """
        Save profile to JSON file.

        Args:
            filepath: Path to save JSON file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> 'TextProfile':
        """
        Create profile from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            TextProfile instance
        """
        return cls(
            name=data['name'],
            features=data['features'],
            text_length=data.get('text_length', 0)
        )

    @classmethod
    def from_json(cls, filepath: str) -> 'TextProfile':
        """
        Load profile from JSON file.

        Args:
            filepath: Path to JSON file

        Returns:
            TextProfile instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __repr__(self):
        return f"TextProfile(name='{self.name}', features={len(self.features)}, length={self.text_length})"
