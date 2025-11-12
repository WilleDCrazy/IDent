"""
Visualization functions for text style analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Tuple
from ident.profile import TextProfile


def visualize_profiles_2d(profiles: List[TextProfile],
                          method: str = 'pca',
                          title: str = 'Text Style Comparison',
                          figsize: Tuple[int, int] = (12, 8),
                          save_path: Optional[str] = None,
                          **kwargs):
    """
    Visualize text profiles in 2D space using PCA dimensionality reduction.

    Args:
        profiles: List of TextProfile objects
        method: Dimensionality reduction method (only 'pca' supported - t-SNE removed due to poor performance)
        title: Plot title
        figsize: Figure size (width, height)
        save_path: Optional path to save the figure
        **kwargs: Additional arguments (reserved for future extensions)
    """
    if len(profiles) < 2:
        raise ValueError("At least 2 profiles required for visualization")

    # Get common features
    common_features = set(profiles[0].features.keys())
    for profile in profiles[1:]:
        common_features &= set(profile.features.keys())

    common_features = sorted(common_features)

    if not common_features:
        raise ValueError("No common features found across profiles")

    # Create feature matrix
    X = np.array([p.get_feature_vector(common_features) for p in profiles])
    names = [p.name for p in profiles]

    # Normalize features
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Apply PCA dimensionality reduction
    if method.lower() != 'pca':
        print(f"Warning: Only 'pca' is supported. t-SNE was removed due to poor performance. Using PCA.")

    from sklearn.decomposition import PCA
    reducer = PCA(n_components=2)
    X_2d = reducer.fit_transform(X_scaled)

    # Get variance explained
    var_explained = reducer.explained_variance_ratio_
    xlabel = f'PC1 ({var_explained[0]:.1%} variance)'
    ylabel = f'PC2 ({var_explained[1]:.1%} variance)'

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)

    # Plot points
    scatter = ax.scatter(X_2d[:, 0], X_2d[:, 1],
                        s=200, alpha=0.6, c=range(len(profiles)),
                        cmap='tab20', edgecolors='black', linewidth=1.5)

    # Add labels
    for i, name in enumerate(names):
        ax.annotate(name, (X_2d[i, 0], X_2d[i, 1]),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                           edgecolor='gray', alpha=0.7))

    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()

    return fig, ax


def plot_feature_comparison(profiles: List[TextProfile],
                           features: Optional[List[str]] = None,
                           top_n: int = 10,
                           figsize: Tuple[int, int] = (14, 8),
                           save_path: Optional[str] = None):
    """
    Create a bar plot comparing specific features across profiles.

    Args:
        profiles: List of TextProfile objects
        features: List of feature names to compare (if None, use most variable)
        top_n: Number of features to show if features is None
        figsize: Figure size
        save_path: Optional path to save the figure
    """
    if not profiles:
        raise ValueError("At least 1 profile required")

    # Get common features
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

    # Prepare data
    names = [p.name for p in profiles]
    data = {name: [p.features.get(f, 0.0) for f in features] for name, p in zip(names, profiles)}

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)

    x = np.arange(len(features))
    width = 0.8 / len(profiles)

    for i, (name, values) in enumerate(data.items()):
        offset = (i - len(profiles) / 2) * width + width / 2
        ax.bar(x + offset, values, width, label=name, alpha=0.8)

    # Format feature names
    formatted_features = [f.replace('_', ' ').title() for f in features]

    ax.set_xlabel('Features', fontsize=12, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title('Feature Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(formatted_features, rotation=45, ha='right')
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()

    return fig, ax


def plot_similarity_heatmap(profiles: List[TextProfile],
                           method: str = 'cosine',
                           figsize: Tuple[int, int] = (10, 8),
                           save_path: Optional[str] = None):
    """
    Create a heatmap of similarity scores between profiles.

    Args:
        profiles: List of TextProfile objects
        method: Comparison method ('cosine', 'euclidean', 'manhattan')
        figsize: Figure size
        save_path: Optional path to save the figure
    """
    from ident.comparator import compare_multiple_profiles

    # Get similarity matrix
    similarity_df = compare_multiple_profiles(profiles, method=method)

    # Create heatmap
    fig, ax = plt.subplots(figsize=figsize)

    # Determine color scheme based on method
    if method == 'cosine':
        cmap = 'RdYlGn'  # Green for high similarity
        vmin, vmax = 0, 1
        fmt = '.3f'
    else:
        cmap = 'RdYlGn_r'  # Green for low distance
        vmin, vmax = None, None
        fmt = '.2f'

    sns.heatmap(similarity_df, annot=True, fmt=fmt, cmap=cmap,
                vmin=vmin, vmax=vmax, square=True, linewidths=0.5,
                cbar_kws={'label': f'{method.capitalize()} Similarity'},
                ax=ax)

    ax.set_title(f'Text Style Similarity Matrix ({method.capitalize()})',
                fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()

    return fig, ax


def plot_feature_distribution(profiles: List[TextProfile],
                             feature_name: str,
                             figsize: Tuple[int, int] = (10, 6),
                             save_path: Optional[str] = None):
    """
    Plot the distribution of a single feature across profiles.

    Args:
        profiles: List of TextProfile objects
        feature_name: Name of the feature to plot
        figsize: Figure size
        save_path: Optional path to save the figure
    """
    # Extract feature values
    names = []
    values = []

    for profile in profiles:
        if feature_name in profile.features:
            names.append(profile.name)
            values.append(profile.features[feature_name])

    if not values:
        raise ValueError(f"Feature '{feature_name}' not found in any profile")

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)

    colors = plt.cm.tab20(np.linspace(0, 1, len(names)))
    bars = ax.bar(range(len(names)), values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    ax.set_xlabel('Text', fontsize=12, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')

    formatted_name = feature_name.replace('_', ' ').title()
    ax.set_title(f'Distribution of {formatted_name}', fontsize=14, fontweight='bold', pad=20)

    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
               f'{value:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()

    return fig, ax


def plot_radar_chart(profiles: List[TextProfile],
                    features: Optional[List[str]] = None,
                    top_n: int = 8,
                    figsize: Tuple[int, int] = (10, 10),
                    save_path: Optional[str] = None):
    """
    Create a radar chart comparing profiles across multiple features.

    Args:
        profiles: List of TextProfile objects (max 5 for readability)
        features: List of feature names (if None, use most variable)
        top_n: Number of features if features is None
        figsize: Figure size
        save_path: Optional path to save the figure
    """
    if len(profiles) > 5:
        print("Warning: More than 5 profiles may make the radar chart hard to read")

    # Get common features
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

        sorted_features = sorted(feature_variances.items(), key=lambda x: x[1], reverse=True)
        features = [name for name, _ in sorted_features[:top_n]]

    # Normalize feature values to 0-1 range for radar chart
    normalized_data = {}
    for feature in features:
        values = [p.features.get(feature, 0.0) for p in profiles]
        min_val, max_val = min(values), max(values)
        if max_val - min_val > 0:
            normalized = [(v - min_val) / (max_val - min_val) for v in values]
        else:
            normalized = [0.5] * len(values)
        normalized_data[feature] = normalized

    # Set up radar chart
    angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))

    # Plot each profile
    colors = plt.cm.tab10(np.linspace(0, 1, len(profiles)))

    for i, profile in enumerate(profiles):
        values = [normalized_data[f][i] for f in features]
        values += values[:1]  # Complete the circle

        ax.plot(angles, values, 'o-', linewidth=2, label=profile.name, color=colors[i])
        ax.fill(angles, values, alpha=0.15, color=colors[i])

    # Format feature names
    formatted_features = [f.replace('_', ' ').title() for f in features]
    formatted_features += formatted_features[:1]

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(formatted_features, size=10)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['0.25', '0.5', '0.75', '1.0'], size=8)
    ax.grid(True, linestyle='--', alpha=0.7)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), framealpha=0.9)
    ax.set_title('Text Style Radar Comparison', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()

    return fig, ax
