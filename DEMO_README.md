# IDent Demo Site

A dark, cryptographic-styled web application for Swedish text style analysis.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will start on `http://localhost:5000`

## Features

- **Landing Page** (`/`): Introduction to IDent technology
- **Demo Page** (`/demo`): Interactive text comparison and analysis
- **About Page** (`/about`): Technical details and methodology

## Demo Page Usage

1. Add 2 or more Swedish text samples (400+ words recommended)
2. Click "Analyze Texts" to process
3. View results in three tabs:
   - **Visualization**: 2D plot using PCA or t-SNE
   - **Similarity**: Pairwise similarity matrix
   - **Features**: Detailed feature comparison across texts

## Technology

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, Plotly.js for visualization
- **Analysis**: scikit-learn for dimensionality reduction
- **Features**: 67+ linguistic and stylometric features

## Design

Dark, cryptographic aesthetic inspired by Palantir with:
- Clean typography (Inter, JetBrains Mono)
- Subtle animations and transitions
- High contrast, professional appearance
- Subject-independent writing style analysis
