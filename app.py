"""
IDent Demo Site - Flask Application
A dark, cryptographic-styled demo for Swedish text style analysis
"""

from flask import Flask, render_template, request, jsonify
from ident import StyleAnalyzer
import numpy as np
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the style analyzer
analyzer = StyleAnalyzer()


@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/demo')
def demo():
    """Interactive demo page"""
    return render_template('demo.html')


@app.route('/about')
def about():
    """About page explaining the technology"""
    return render_template('about.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_texts():
    """
    Analyze multiple texts and return profiles with 2D visualization data

    Expected JSON:
    {
        "texts": [
            {"name": "Text 1", "content": "..."},
            {"name": "Text 2", "content": "..."}
        ]
    }
    """
    try:
        data = request.get_json()

        if not data or 'texts' not in data:
            return jsonify({'error': 'No texts provided'}), 400

        texts = data['texts']

        if len(texts) < 2:
            return jsonify({'error': 'At least 2 texts are required for comparison'}), 400

        # Analyze each text
        profiles = []
        for text_data in texts:
            name = text_data.get('name', f'Text {len(profiles) + 1}')
            content = text_data.get('content', '')

            if not content.strip():
                return jsonify({'error': f'Text "{name}" is empty'}), 400

            # Analyze the text
            profile = analyzer.analyze(content, name=name)
            profiles.append(profile)

        # Create 2D projection for visualization
        projection_data = create_2d_projection(profiles, method='pca')

        # Also create t-SNE projection if we have enough samples
        tsne_data = None
        if len(profiles) >= 3:
            try:
                tsne_data = create_2d_projection(profiles, method='tsne')
            except:
                pass  # t-SNE might fail with few samples

        # Build response with profiles and visualization data
        response = {
            'profiles': [],
            'visualization': {
                'pca': projection_data,
                'tsne': tsne_data
            },
            'similarity_matrix': calculate_similarity_matrix(profiles)
        }

        # Extract key features from each profile
        for profile in profiles:
            profile_data = {
                'name': profile.name,
                'features': {
                    'lexical': {
                        'total_words': profile.features.get('total_words', 0),
                        'unique_words': profile.features.get('unique_words', 0),
                        'type_token_ratio': round(profile.features.get('type_token_ratio', 0), 4),
                        'avg_word_length': round(profile.features.get('avg_word_length', 0), 2),
                        'lexical_density': round(profile.features.get('lexical_density', 0), 4),
                        'mtld': round(profile.features.get('mtld', 0), 2)
                    },
                    'syntactic': {
                        'total_sentences': profile.features.get('total_sentences', 0),
                        'avg_sentence_length': round(profile.features.get('avg_sentence_length', 0), 2),
                        'punctuation_frequency': round(profile.features.get('punctuation_frequency', 0), 4),
                        'comma_density': round(profile.features.get('comma_density', 0), 4)
                    },
                    'stylometric': {
                        'yules_k': round(profile.features.get('yules_k', 0), 2),
                        'simpsons_d': round(profile.features.get('simpsons_d', 0), 4),
                        'entropy': round(profile.features.get('entropy', 0), 4),
                        'burstiness': round(profile.features.get('burstiness', 0), 4)
                    },
                    'swedish': {
                        'swedish_char_frequency': round(profile.features.get('swedish_char_frequency', 0), 4),
                        'compound_word_ratio': round(profile.features.get('compound_word_ratio', 0), 4),
                        'function_word_ratio': round(profile.features.get('function_word_ratio', 0), 4)
                    }
                },
                'all_features': profile.features
            }
            response['profiles'].append(profile_data)

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def calculate_similarity_matrix(profiles):
    """Calculate pairwise similarity matrix for all profiles"""
    n = len(profiles)
    matrix = []

    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                similarity = 1.0
            else:
                # Use cosine similarity (higher = more similar)
                similarity = profiles[i].compare(profiles[j], method='cosine')
            row.append(round(similarity, 4))
        matrix.append(row)

    return matrix


def create_2d_projection(profiles, method='pca'):
    """Create 2D projection of text profiles"""
    if len(profiles) < 2:
        return None

    # Extract feature vectors
    feature_vectors = []
    for profile in profiles:
        # Get all numeric features
        features = []
        for key in sorted(profile.features.keys()):
            val = profile.features[key]
            if isinstance(val, (int, float)) and not np.isnan(val) and not np.isinf(val):
                features.append(val)
        feature_vectors.append(features)

    # Convert to numpy array
    X = np.array(feature_vectors)

    # Normalize features
    from sklearn.preprocessing import StandardScaler
    X_scaled = StandardScaler().fit_transform(X)

    # Apply dimensionality reduction
    if method == 'pca':
        from sklearn.decomposition import PCA
        reducer = PCA(n_components=2)
        X_2d = reducer.fit_transform(X_scaled)
        variance_explained = reducer.explained_variance_ratio_.tolist()
    elif method == 'tsne':
        from sklearn.manifold import TSNE
        # Adjust perplexity based on number of samples
        perplexity = min(30, max(2, len(profiles) - 1))
        reducer = TSNE(n_components=2, perplexity=perplexity, random_state=42)
        X_2d = reducer.fit_transform(X_scaled)
        variance_explained = None
    else:
        raise ValueError(f"Unknown method: {method}")

    # Build visualization data
    points = []
    for i, profile in enumerate(profiles):
        points.append({
            'name': profile.name,
            'x': float(X_2d[i, 0]),
            'y': float(X_2d[i, 1])
        })

    return {
        'method': method,
        'points': points,
        'variance_explained': variance_explained
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
