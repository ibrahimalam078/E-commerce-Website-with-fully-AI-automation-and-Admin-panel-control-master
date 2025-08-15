"""
Admin Panel Integration Examples for AI Automation System
Python examples for integrating with various admin panel frameworks
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class AIAutomationClient:
    """Python client for AI Automation System API"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def check_health(self) -> Dict:
        """Check API health status"""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()
    
    # ==================== PRODUCT AUTOMATION ====================
    
    def automate_product_setup(self, product_data: Dict) -> Dict:
        """Complete product automation pipeline"""
        response = self.session.post(
            f"{self.base_url}/api/complete-product-automation",
            json=product_data
        )
        return response.json()
    
    def generate_product_description(self, product_name: str, features: List[str], 
                                   category: str = None, image_description: str = None) -> Dict:
        """Generate AI-powered product description"""
        payload = {
            "product_name": product_name,
            "features": features,
            "category": category,
            "image_description": image_description
        }
        response = self.session.post(f"{self.base_url}/api/generate-description", json=payload)
        return response.json()
    
    def generate_seo_metadata(self, product_name: str, description: str, 
                            category: str = None, price: float = None) -> Dict:
        """Generate SEO-optimized metadata"""
        payload = {
            "product_name": product_name,
            "description": description,
            "category": category,
            "price": price
        }
        response = self.session.post(f"{self.base_url}/api/generate-seo", json=payload)
        return response.json()
    
    def generate_categories(self, product_name: str, description: str = None, 
                          image_description: str = None) -> Dict:
        """Generate product categories and tags"""
        payload = {
            "product_name": product_name,
            "description": description,
            "image_description": image_description
        }
        response = self.session.post(f"{self.base_url}/api/generate-categories", json=payload)
        return response.json()
    
    # ==================== IMAGE ANALYSIS ====================
    
    def analyze_product_image(self, image_source: str, source_type: str = "url") -> Dict:
        """Analyze product image with BLIP AI"""
        payload = {
            "image_source": image_source,
            "source_type": source_type
        }
        response = self.session.post(f"{self.base_url}/api/analyze-image", json=payload)
        return response.json()
    
    def generate_alt_text(self, image_source: str, product_name: str = None, 
                         source_type: str = "url") -> Dict:
        """Generate SEO-friendly alt text for images"""
        payload = {
            "image_source": image_source,
            "source_type": source_type,
            "product_name": product_name
        }
        response = self.session.post(f"{self.base_url}/api/generate-alt-text", json=payload)
        return response.json()
    
    # ==================== RECOMMENDATIONS ====================
    
    def train_recommendation_model(self, use_sample_data: bool = True, algorithm: str = "NMF") -> Dict:
        """Train recommendation model"""
        payload = {
            "use_sample_data": use_sample_data,
            "algorithm": algorithm
        }
        response = self.session.post(f"{self.base_url}/api/train-recommendations", json=payload)
        return response.json()
    
    def get_user_recommendations(self, user_id: str, n_recommendations: int = 10, 
                               exclude_rated: bool = True) -> Dict:
        """Get personalized recommendations for a user"""
        params = {
            'n_recommendations': n_recommendations,
            'exclude_rated': str(exclude_rated).lower()
        }
        response = self.session.get(f"{self.base_url}/api/user-recommendations/{user_id}", params=params)
        return response.json()
    
    def get_similar_products(self, product_id: str, n_recommendations: int = 10) -> Dict:
        """Get similar product recommendations"""
        params = {'n_recommendations': n_recommendations}
        response = self.session.get(f"{self.base_url}/api/item-recommendations/{product_id}", params=params)
        return response.json()
    
    def get_popular_products(self, n_items: int = 10, min_ratings: int = 5) -> Dict:
        """Get most popular products"""
        params = {
            'n_items': n_items,
            'min_ratings': min_ratings
        }
        response = self.session.get(f"{self.base_url}/api/popular-items", params=params)
        return response.json()
    
    def predict_user_rating(self, user_id: str, item_id: str) -> Dict:
        """Predict user rating for a product"""
        payload = {
            "user_id": user_id,
            "item_id": item_id
        }
        response = self.session.post(f"{self.base_url}/api/predict-rating", json=payload)
        return response.json()
    
    # ==================== CONTENT MARKETING ====================
    
    def generate_blog_content(self, topic: str, products: List[str] = None, 
                            target_audience: str = None, content_type: str = "article") -> Dict:
        """Generate blog/article content"""
        payload = {
            "topic": topic,
            "products": products or [],
            "target_audience": target_audience,
            "content_type": content_type
        }
        response = self.session.post(f"{self.base_url}/api/generate-blog", json=payload)
        return response.json()
    
    def generate_pricing_strategy(self, product_name: str, category: str, current_price: float,
                                competitor_prices: List[float] = None, demand_level: str = "medium") -> Dict:
        """Generate AI-powered pricing strategy"""
        payload = {
            "product_name": product_name,
            "category": category,
            "current_price": current_price,
            "competitor_prices": competitor_prices or [],
            "demand_level": demand_level
        }
        response = self.session.post(f"{self.base_url}/api/generate-pricing", json=payload)
        return response.json()


# ==================== DJANGO INTEGRATION EXAMPLE ====================

def django_product_automation_view(request):
    """Django view example for product automation"""
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_http_methods
    
    @csrf_exempt
    @require_http_methods(["POST"])
    def handle_request(request):
        try:
            # Initialize AI client
            ai_client = AIAutomationClient()
            
            # Parse request data
            data = json.loads(request.body)
            product_name = data.get('product_name')
            features = data.get('features', [])
            image_url = data.get('image_url')
            category = data.get('category')
            price = data.get('price')
            
            if not product_name:
                return JsonResponse({'error': 'Product name is required'}, status=400)
            
            # Run complete automation
            automation_result = ai_client.automate_product_setup({
                'product_name': product_name,
                'features': features,
                'category': category,
                'price': price,
                'image_source': image_url,
                'source_type': 'url' if image_url else None
            })
            
            if automation_result.get('success'):
                # Process the results for your Django models
                ai_data = automation_result['data']
                
                # Example: Save to Django models
                # product = Product.objects.create(
                #     name=product_name,
                #     description=ai_data.get('description', {}).get('description'),
                #     seo_title=ai_data.get('seo_metadata', {}).get('seo_title'),
                #     meta_description=ai_data.get('seo_metadata', {}).get('meta_description'),
                #     category=category,
                #     price=price
                # )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Product automated successfully',
                    'ai_data': ai_data
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'AI automation failed'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return handle_request(request)


# ==================== FLASK ADMIN INTEGRATION EXAMPLE ====================

def flask_admin_integration():
    """Flask-Admin integration example"""
    from flask import Flask, request, jsonify, render_template
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
    
    class AIAutomatedProductView(ModelView):
        """Custom Flask-Admin view with AI automation"""
        
        def __init__(self, model, session, **kwargs):
            super().__init__(model, session, **kwargs)
            self.ai_client = AIAutomationClient()
        
        def create_model(self, form):
            """Override create to add AI automation"""
            try:
                # Create the base model
                model = super().create_model(form)
                
                if model:
                    # Run AI automation
                    automation_result = self.ai_client.automate_product_setup({
                        'product_name': model.name,
                        'features': form.features.data.split(',') if form.features.data else [],
                        'category': model.category,
                        'price': float(model.price) if model.price else None,
                        'image_source': model.image_url
                    })
                    
                    if automation_result.get('success'):
                        ai_data = automation_result['data']
                        
                        # Update model with AI-generated content
                        if 'description' in ai_data:
                            model.description = ai_data['description'].get('description', model.description)
                        
                        if 'seo_metadata' in ai_data:
                            seo = ai_data['seo_metadata']
                            model.seo_title = seo.get('seo_title')
                            model.meta_description = seo.get('meta_description')
                        
                        if 'categories_tags' in ai_data:
                            cats = ai_data['categories_tags']
                            model.primary_category = cats.get('primary_category')
                            model.tags = ', '.join(cats.get('tags', [])[:10])  # Limit tags
                        
                        # Save updates
                        self.session.commit()
                
                return model
                
            except Exception as e:
                self.session.rollback()
                return None


# ==================== FASTAPI INTEGRATION EXAMPLE ====================

def fastapi_integration_example():
    """FastAPI integration example"""
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from pydantic import BaseModel
    from typing import Optional
    
    app = FastAPI(title="E-commerce Admin with AI")
    ai_client = AIAutomationClient()
    
    class ProductCreate(BaseModel):
        name: str
        features: List[str] = []
        category: Optional[str] = None
        price: Optional[float] = None
        image_url: Optional[str] = None
    
    class RecommendationRequest(BaseModel):
        user_id: str
        n_recommendations: int = 10
    
    @app.post("/products/automate")
    async def automate_product_creation(product: ProductCreate, background_tasks: BackgroundTasks):
        """Automate product creation with AI"""
        try:
            # Start automation process
            automation_data = {
                'product_name': product.name,
                'features': product.features,
                'category': product.category,
                'price': product.price,
                'image_source': product.image_url,
                'source_type': 'url' if product.image_url else None
            }
            
            # Run automation
            result = ai_client.automate_product_setup(automation_data)
            
            if result.get('success'):
                # Add background task to process recommendations
                background_tasks.add_task(update_recommendations_cache)
                
                return {
                    "message": "Product automation completed",
                    "ai_generated_data": result['data']
                }
            else:
                raise HTTPException(status_code=500, detail="AI automation failed")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/recommendations/{user_id}")
    async def get_user_recommendations(user_id: str, n_recommendations: int = 10):
        """Get personalized recommendations"""
        try:
            result = ai_client.get_user_recommendations(user_id, n_recommendations)
            
            if result.get('success'):
                return result['data']
            else:
                raise HTTPException(status_code=500, detail="Failed to get recommendations")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def update_recommendations_cache():
        """Background task to update recommendation cache"""
        # Implement caching logic here
        pass


# ==================== JAVASCRIPT INTEGRATION EXAMPLES ====================

def generate_javascript_examples():
    """Generate JavaScript integration examples"""
    
    js_code = '''
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
'''
    
    return js_code


# ==================== EXAMPLE USAGE DEMONSTRATIONS ====================

def demonstrate_integrations():
    """Demonstrate various integration scenarios"""
    print("🔗 AI Automation System - Admin Panel Integration Examples")
    print("=" * 70)
    
    # Initialize client
    ai_client = AIAutomationClient()
    
    try:
        # Test connection
        health = ai_client.check_health()
        print(f"✅ API Health: {health.get('status', 'Unknown')}")
        
        print("\n🛍️ Example 1: New Product Setup")
        print("-" * 40)
        
        # Example product automation
        product_data = {
            "product_name": "Premium Rosehip Seed Oil",
            "features": ["100% pure", "cold-pressed", "anti-aging", "vitamin C rich"],
            "category": "Skincare Oils",
            "price": 34.99,
            "image_source": "https://example.com/rosehip-oil.jpg"
        }
        
        print(f"📦 Product: {product_data['product_name']}")
        print(f"💰 Price: ${product_data['price']}")
        print(f"🏷️ Category: {product_data['category']}")
        
        # In a real admin panel, you'd call:
        # result = ai_client.automate_product_setup(product_data)
        print("✅ AI automation would generate: description, SEO metadata, categories, tags")
        
        print("\n👤 Example 2: User Personalization")  
        print("-" * 40)
        
        user_id = "user_12345"
        print(f"🔍 Getting recommendations for user: {user_id}")
        
        # In a real admin panel, you'd call:
        # recommendations = ai_client.get_user_recommendations(user_id, 5)
        print("✅ AI would return personalized product recommendations")
        
        print("\n🔗 Example 3: Product Cross-selling")
        print("-" * 40)
        
        product_id = "Premium Rosehip Seed Oil"
        print(f"🔍 Finding similar products to: {product_id}")
        
        # In a real admin panel, you'd call:
        # similar = ai_client.get_similar_products(product_id, 6)
        print("✅ AI would return similar products for cross-selling")
        
        print("\n📊 Integration Summary:")
        print("  • Python Client: Ready for Django, Flask, FastAPI")
        print("  • JavaScript API: Ready for frontend integration")
        print("  • REST Endpoints: Compatible with any framework")
        print("  • Real-time Processing: Immediate AI responses")
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        print("   Note: Ensure the Flask server is running first")

if __name__ == "__main__":
    # Generate JavaScript examples
    js_examples = generate_javascript_examples()
    
    # Save JavaScript examples to file
    with open('admin_panel_integration.js', 'w') as f:
        f.write(js_examples)
    
    print("✅ Generated JavaScript integration examples")
    
    # Demonstrate integrations
    demonstrate_integrations()
