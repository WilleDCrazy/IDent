"""
Profile comparison and similarity analysis.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional
from ident.profile import TextProfile


def compare_multiple_profiles(profiles: List[TextProfile],
                              method: str = 'cosine') -> pd.DataFrame:
    """
    Create a similarity matrix comparing all profiles.

    Args:
        profiles: List of TextProfile objects
        method: Comparison method ('cosine', 'euclidean', 'manhattan')

    Returns:
        Pandas DataFrame with similarity matrix
    """
    n = len(profiles)
    names = [p.name for p in profiles]

    # Create similarity matrix
    similarity_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                # Same profile
                similarity_matrix[i, j] = 1.0 if method == 'cosine' else 0.0
            else:
                similarity = profiles[i].compare(profiles[j], method=method)
                similarity_matrix[i, j] = similarity

    # Create DataFrame
    df = pd.DataFrame(similarity_matrix, index=names, columns=names)

    return df


def find_most_similar(profile: TextProfile,
                      candidates: List[TextProfile],
                      method: str = 'cosine',
                      top_n: int = 5) -> List[tuple]:
    """
    Find the most similar profiles to a given profile.

    Args:
        profile: The reference TextProfile
        candidates: List of candidate TextProfiles to compare
        method: Comparison method
        top_n: Number of top matches to return

    Returns:
        List of tuples (profile, similarity_score) sorted by similarity
    """
    similarities = []

    for candidate in candidates:
        if candidate.name != profile.name:  # Skip self
            similarity = profile.compare(candidate, method=method)
            similarities.append((candidate, similarity))

    # Sort based on method
    if method == 'cosine':
        # Higher is better for cosine
        similarities.sort(key=lambda x: x[1], reverse=True)
    else:
        # Lower is better for distance metrics
        similarities.sort(key=lambda x: x[1])

    return similarities[:top_n]


def get_distinctive_features(profile1: TextProfile,
                            profile2: TextProfile,
                            top_n: int = 10) -> Dict[str, tuple]:
    """
    Find the most distinctive features between two profiles.

    Args:
        profile1: First TextProfile
        profile2: Second TextProfile
        top_n: Number of top distinctive features to return

    Returns:
        Dictionary mapping feature names to (value1, value2, difference)
    """
    # Get common features
    common_features = set(profile1.features.keys()) & set(profile2.features.keys())

    # Calculate differences
    differences = {}
    for feature in common_features:
        val1 = profile1.features[feature]
        val2 = profile2.features[feature]
        diff = abs(val1 - val2)
        differences[feature] = (val1, val2, diff)

    # Sort by difference
    sorted_features = sorted(differences.items(), key=lambda x: x[1][2], reverse=True)

    # Return top N
    result = {name: values for name, values in sorted_features[:top_n]}

    return result


def create_feature_comparison_table(profiles: List[TextProfile],
                                   features: Optional[List[str]] = None,
                                   top_n: int = 15) -> pd.DataFrame:
    """
    Create a table comparing specific features across profiles.

    Args:
        profiles: List of TextProfile objects
        features: List of feature names to compare (if None, use most variable features)
        top_n: If features is None, select top N most variable features

    Returns:
        Pandas DataFrame with feature comparison
    """
    if not profiles:
        return pd.DataFrame()

    # Get all common features
    common_features = set(profiles[0].features.keys())
    for profile in profiles[1:]:
        common_features &= set(profile.features.keys())

    common_features = sorted(common_features)

    if features is None:
        # Select most variable features
        feature_variances = {}
        for feature in common_features:
            values = [p.features[feature] for p in profiles]
            variance = np.var(values)
            feature_variances[feature] = variance

        # Get top N by variance
        sorted_features = sorted(feature_variances.items(), key=lambda x: x[1], reverse=True)
        features = [name for name, _ in sorted_features[:top_n]]

    # Create DataFrame
    data = {}
    for profile in profiles:
        data[profile.name] = [profile.features.get(f, 0.0) for f in features]

    df = pd.DataFrame(data, index=features)

    return df


def calculate_profile_centroid(profiles: List[TextProfile]) -> Dict[str, float]:
    """
    Calculate the centroid (average) of multiple profiles.

    Args:
        profiles: List of TextProfile objects

    Returns:
        Dictionary of average feature values
    """
    if not profiles:
        return {}

    # Get common features
    common_features = set(profiles[0].features.keys())
    for profile in profiles[1:]:
        common_features &= set(profile.features.keys())

    # Calculate averages
    centroid = {}
    for feature in common_features:
        values = [p.features[feature] for p in profiles]
        centroid[feature] = np.mean(values)

    return centroid


def calculate_profile_deviation(profile: TextProfile,
                               centroid: Dict[str, float]) -> float:
    """
    Calculate how much a profile deviates from a centroid.

    Args:
        profile: TextProfile to compare
        centroid: Centroid dictionary (from calculate_profile_centroid)

    Returns:
        Euclidean distance from centroid
    """
    common_features = set(profile.features.keys()) & set(centroid.keys())

    if not common_features:
        return 0.0

    # Calculate Euclidean distance
    distances = []
    for feature in common_features:
        diff = profile.features[feature] - centroid[feature]
        distances.append(diff ** 2)

    return np.sqrt(np.mean(distances))


def cluster_profiles(profiles: List[TextProfile],
                    n_clusters: int = 2,
                    method: str = 'kmeans') -> Dict[int, List[TextProfile]]:
    """
    Cluster profiles into groups.

    Args:
        profiles: List of TextProfile objects
        n_clusters: Number of clusters
        method: Clustering method ('kmeans' only for now)

    Returns:
        Dictionary mapping cluster ID to list of profiles
    """
    if len(profiles) < n_clusters:
        raise ValueError("Number of profiles must be >= number of clusters")

    try:
        from sklearn.cluster import KMeans
    except ImportError:
        raise ImportError("scikit-learn is required for clustering")

    # Get common features
    common_features = set(profiles[0].features.keys())
    for profile in profiles[1:]:
        common_features &= set(profile.features.keys())

    common_features = sorted(common_features)

    # Create feature matrix
    X = np.array([p.get_feature_vector(common_features) for p in profiles])

    # Normalize features
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform clustering
    if method == 'kmeans':
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
    else:
        raise ValueError(f"Unknown clustering method: {method}")

    # Group profiles by cluster
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(profiles[i])

    return clusters
