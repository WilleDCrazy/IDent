// Demo page interactivity

class DemoApp {
    constructor() {
        this.texts = [];
        this.results = null;
        this.currentVizMethod = 'pca';

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.addTextInput(); // Start with one text input
        this.addTextInput(); // Start with two text inputs
    }

    setupEventListeners() {
        // Add text button
        document.getElementById('addTextBtn').addEventListener('click', () => {
            this.addTextInput();
        });

        // Analyze button
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.analyzeTexts();
        });

        // Clear button
        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearAll();
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchTab(btn.dataset.tab);
            });
        });

        // Visualization method switching
        document.querySelectorAll('input[name="vizMethod"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentVizMethod = e.target.value;
                if (this.results) {
                    this.renderVisualization();
                }
            });
        });
    }

    addTextInput() {
        const container = document.getElementById('textsContainer');
        const index = this.texts.length;

        const textGroup = document.createElement('div');
        textGroup.className = 'text-input-group';
        textGroup.dataset.index = index;

        textGroup.innerHTML = `
            <div class="text-input-header">
                <label class="text-input-label">Text ${index + 1}</label>
                <button class="remove-text-btn" onclick="demoApp.removeTextInput(${index})">×</button>
            </div>
            <input type="text" class="text-name-input" placeholder="Text name (optional)"
                   value="Text ${index + 1}" data-index="${index}">
            <textarea class="text-content-input" placeholder="Paste Swedish text here (400+ words recommended)"
                      data-index="${index}"></textarea>
        `;

        container.appendChild(textGroup);

        this.texts.push({
            name: `Text ${index + 1}`,
            content: ''
        });

        // Add event listeners for input changes
        const nameInput = textGroup.querySelector('.text-name-input');
        const contentInput = textGroup.querySelector('.text-content-input');

        nameInput.addEventListener('input', (e) => {
            this.texts[index].name = e.target.value || `Text ${index + 1}`;
        });

        contentInput.addEventListener('input', (e) => {
            this.texts[index].content = e.target.value;
            this.updateAnalyzeButton();
        });

        this.updateAnalyzeButton();
    }

    removeTextInput(index) {
        const container = document.getElementById('textsContainer');
        const textGroup = container.querySelector(`[data-index="${index}"]`);
        if (textGroup) {
            textGroup.remove();
        }

        this.texts[index] = null; // Mark as removed
        this.updateAnalyzeButton();

        // If less than 2 valid texts, hide results
        const validTexts = this.texts.filter(t => t && t.content.trim());
        if (validTexts.length < 2) {
            this.hideResults();
        }
    }

    updateAnalyzeButton() {
        const validTexts = this.texts.filter(t => t && t.content.trim());
        const analyzeBtn = document.getElementById('analyzeBtn');
        analyzeBtn.disabled = validTexts.length < 2;
    }

    clearAll() {
        const container = document.getElementById('textsContainer');
        container.innerHTML = '';
        this.texts = [];
        this.results = null;
        this.hideResults();
        this.hideError();

        // Add back two empty inputs
        this.addTextInput();
        this.addTextInput();
    }

    async analyzeTexts() {
        this.hideError();
        this.showLoading();

        const validTexts = this.texts
            .filter(t => t && t.content.trim())
            .map(t => ({
                name: t.name,
                content: t.content
            }));

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ texts: validTexts })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Analysis failed');
            }

            this.results = await response.json();
            this.hideLoading();
            this.showResults();
            this.renderAllResults();

        } catch (error) {
            this.hideLoading();
            this.showError(error.message);
        }
    }

    renderAllResults() {
        this.renderVisualization();
        this.renderSimilarityMatrix();
        this.renderFeatures();
    }

    renderVisualization() {
        const vizData = this.results.visualization[this.currentVizMethod];

        if (!vizData || !vizData.points) {
            document.getElementById('visualizationPlot').innerHTML =
                '<p style="text-align: center; color: var(--text-tertiary); padding: 2rem;">Visualization not available</p>';
            return;
        }

        const points = vizData.points;

        // Create Plotly scatter plot
        const trace = {
            x: points.map(p => p.x),
            y: points.map(p => p.y),
            mode: 'markers+text',
            type: 'scatter',
            text: points.map(p => p.name),
            textposition: 'top center',
            textfont: {
                family: 'Inter, sans-serif',
                size: 12,
                color: '#e8e8e8'
            },
            marker: {
                size: 12,
                color: '#00c9ff',
                line: {
                    color: '#0099cc',
                    width: 2
                }
            },
            hovertemplate: '<b>%{text}</b><br>X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>'
        };

        const layout = {
            paper_bgcolor: '#0a0a0a',
            plot_bgcolor: '#0a0a0a',
            font: {
                family: 'Inter, sans-serif',
                color: '#a0a0a0'
            },
            xaxis: {
                title: this.currentVizMethod === 'pca' ? 'PC1' : 't-SNE 1',
                gridcolor: '#2a2a2a',
                zerolinecolor: '#333333'
            },
            yaxis: {
                title: this.currentVizMethod === 'pca' ? 'PC2' : 't-SNE 2',
                gridcolor: '#2a2a2a',
                zerolinecolor: '#333333'
            },
            hovermode: 'closest',
            margin: { l: 50, r: 20, t: 20, b: 50 }
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot('visualizationPlot', [trace], layout, config);

        // Show variance explained for PCA
        if (this.currentVizMethod === 'pca' && vizData.variance_explained) {
            const variance = vizData.variance_explained;
            const total = ((variance[0] + variance[1]) * 100).toFixed(1);
            document.getElementById('vizInfo').innerHTML =
                `Variance explained: PC1 ${(variance[0] * 100).toFixed(1)}%, PC2 ${(variance[1] * 100).toFixed(1)}% (Total: ${total}%)`;
        } else {
            document.getElementById('vizInfo').innerHTML = '';
        }
    }

    renderSimilarityMatrix() {
        const matrix = this.results.similarity_matrix;
        const profiles = this.results.profiles;

        let html = '<table class="similarity-table"><thead><tr><th>Text</th>';

        // Header row
        profiles.forEach(p => {
            html += `<th>${this.escapeHtml(p.name)}</th>`;
        });
        html += '</tr></thead><tbody>';

        // Data rows
        profiles.forEach((p, i) => {
            html += `<tr><th>${this.escapeHtml(p.name)}</th>`;
            matrix[i].forEach((similarity, j) => {
                const cssClass = i === j ? 'similarity-high' :
                                 similarity > 0.8 ? 'similarity-high' :
                                 similarity > 0.5 ? 'similarity-medium' : 'similarity-low';
                html += `<td><span class="similarity-value ${cssClass}">${similarity.toFixed(3)}</span></td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table>';
        document.getElementById('similarityMatrix').innerHTML = html;
    }

    renderFeatures() {
        const profiles = this.results.profiles;

        const categories = {
            'Lexical Features': 'lexical',
            'Syntactic Features': 'syntactic',
            'Stylometric Features': 'stylometric',
            'Swedish-Specific Features': 'swedish'
        };

        let html = '';

        Object.entries(categories).forEach(([categoryName, categoryKey]) => {
            html += `
                <div class="feature-category-section">
                    <h3 class="category-title">${categoryName}</h3>
                    <table class="feature-table">
                        <thead>
                            <tr>
                                <th>Feature</th>
                                ${profiles.map(p => `<th>${this.escapeHtml(p.name)}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
            `;

            const features = profiles[0].features[categoryKey];
            Object.keys(features).forEach(featureName => {
                html += `<tr><td>${this.formatFeatureName(featureName)}</td>`;
                profiles.forEach(p => {
                    const value = p.features[categoryKey][featureName];
                    html += `<td>${this.formatValue(value)}</td>`;
                });
                html += '</tr>';
            });

            html += '</tbody></table></div>';
        });

        document.getElementById('featuresComparison').innerHTML = html;
    }

    formatFeatureName(name) {
        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatValue(value) {
        if (typeof value === 'number') {
            return value.toFixed(4);
        }
        return value;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}Tab`);
        });
    }

    showResults() {
        document.getElementById('resultsPlaceholder').style.display = 'none';
        document.getElementById('resultsContent').style.display = 'block';
    }

    hideResults() {
        document.getElementById('resultsPlaceholder').style.display = 'flex';
        document.getElementById('resultsContent').style.display = 'none';
    }

    showLoading() {
        document.getElementById('loadingMessage').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingMessage').style.display = 'none';
    }

    showError(message) {
        const errorEl = document.getElementById('errorMessage');
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }

    hideError() {
        document.getElementById('errorMessage').style.display = 'none';
    }
}

// Initialize the app
let demoApp;
document.addEventListener('DOMContentLoaded', () => {
    demoApp = new DemoApp();
});
