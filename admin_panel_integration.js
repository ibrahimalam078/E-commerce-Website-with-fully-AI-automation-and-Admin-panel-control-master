
// JavaScript Integration Examples for AI Automation System

class AIAutomationAPI {
    constructor(baseUrl = 'http://127.0.0.1:5000') {
        this.baseUrl = baseUrl;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        const response = await fetch(url, config);
        return await response.json();
    }
    
    // ==================== PRODUCT AUTOMATION ====================
    
    async automateProduct(productData) {
        return await this.request('/api/complete-product-automation', {
            method: 'POST',
            body: JSON.stringify(productData)
        });
    }
    
    async generateDescription(productName, features, category, imageDescription) {
        return await this.request('/api/generate-description', {
            method: 'POST',
            body: JSON.stringify({
                product_name: productName,
                features: features,
                category: category,
                image_description: imageDescription
            })
        });
    }
    
    async generateSEO(productName, description, category, price) {
        return await this.request('/api/generate-seo', {
            method: 'POST',
            body: JSON.stringify({
                product_name: productName,
                description: description,
                category: category,
                price: price
            })
        });
    }
    
    // ==================== RECOMMENDATIONS ====================
    
    async getUserRecommendations(userId, nRecommendations = 10) {
        return await this.request(`/api/user-recommendations/${userId}?n_recommendations=${nRecommendations}`);
    }
    
    async getSimilarProducts(productId, nRecommendations = 10) {
        return await this.request(`/api/item-recommendations/${productId}?n_recommendations=${nRecommendations}`);
    }
    
    async getPopularProducts(nItems = 10) {
        return await this.request(`/api/popular-items?n_items=${nItems}`);
    }
    
    // ==================== IMAGE ANALYSIS ====================
    
    async analyzeImage(imageUrl) {
        return await this.request('/api/analyze-image', {
            method: 'POST',
            body: JSON.stringify({
                image_source: imageUrl,
                source_type: 'url'
            })
        });
    }
}

// ==================== ADMIN PANEL INTEGRATION EXAMPLES ====================

class AdminPanelIntegration {
    constructor() {
        this.ai = new AIAutomationAPI();
    }
    
    // Product creation form handler
    async handleProductCreation(formData) {
        try {
            // Show loading state
            this.showLoading('Generating AI content...');
            
            const result = await this.ai.automateProduct({
                product_name: formData.name,
                features: formData.features.split(','),
                category: formData.category,
                price: parseFloat(formData.price),
                image_source: formData.imageUrl
            });
            
            if (result.success) {
                // Populate form fields with AI-generated content
                this.populateFormFields(result.data);
                this.showSuccess('AI automation completed!');
            } else {
                this.showError('Failed to generate AI content');
            }
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }
    
    // Recommendation widget
    async loadRecommendationWidget(userId, containerId) {
        try {
            const result = await this.ai.getUserRecommendations(userId, 5);
            
            if (result.success && result.data.recommendations) {
                const container = document.getElementById(containerId);
                const html = this.generateRecommendationHTML(result.data.recommendations);
                container.innerHTML = html;
            }
        } catch (error) {
            console.error('Failed to load recommendations:', error);
        }
    }
    
    // Product similarity widget
    async loadSimilarProducts(productId, containerId) {
        try {
            const result = await this.ai.getSimilarProducts(productId, 6);
            
            if (result.success && result.data.similar_items) {
                const container = document.getElementById(containerId);
                const html = this.generateSimilarProductsHTML(result.data.similar_items);
                container.innerHTML = html;
            }
        } catch (error) {
            console.error('Failed to load similar products:', error);
        }
    }
    
    // Helper methods
    populateFormFields(aiData) {
        if (aiData.description) {
            document.getElementById('product-description').value = aiData.description.description;
        }
        
        if (aiData.seo_metadata) {
            document.getElementById('seo-title').value = aiData.seo_metadata.seo_title;
            document.getElementById('meta-description').value = aiData.seo_metadata.meta_description;
        }
        
        if (aiData.categories_tags) {
            document.getElementById('category').value = aiData.categories_tags.primary_category;
            document.getElementById('tags').value = aiData.categories_tags.tags.join(', ');
        }
    }
    
    generateRecommendationHTML(recommendations) {
        return recommendations.map(rec => `
            <div class="recommendation-item">
                <h4>${rec.product_id}</h4>
                <span class="rating">Predicted: ${rec.predicted_rating.toFixed(2)}/5</span>
                <span class="confidence">Confidence: ${(rec.confidence * 100).toFixed(0)}%</span>
            </div>
        `).join('');
    }
    
    generateSimilarProductsHTML(similarItems) {
        return similarItems.map(item => `
            <div class="similar-product">
                <h4>${item.product_id}</h4>
                <span class="similarity">Similarity: ${(item.similarity_score * 100).toFixed(0)}%</span>
            </div>
        `).join('');
    }
    
    showLoading(message) {
        // Implement loading UI
        console.log('Loading:', message);
    }
    
    hideLoading() {
        // Hide loading UI
        console.log('Loading complete');
    }
    
    showSuccess(message) {
        // Show success message
        console.log('Success:', message);
    }
    
    showError(message) {
        // Show error message
        console.error('Error:', message);
    }
}

// ==================== USAGE EXAMPLES ====================

// Initialize the integration
const adminIntegration = new AdminPanelIntegration();

// Example: Handle form submission
document.getElementById('product-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await adminIntegration.handleProductCreation(Object.fromEntries(formData));
});

// Example: Load recommendations on user profile page
if (typeof currentUserId !== 'undefined') {
    adminIntegration.loadRecommendationWidget(currentUserId, 'recommendations-container');
}

// Example: Load similar products on product page
if (typeof currentProductId !== 'undefined') {
    adminIntegration.loadSimilarProducts(currentProductId, 'similar-products-container');
}
