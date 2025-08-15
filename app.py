"""
AI Automation System - Flask API
Main application with endpoints for all automation features
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
from datetime import datetime
import os

from config import Config
from services.gemini_service import GeminiService
from services.blip_service import BLIPService
from services.simple_recommendation_service import SimpleRecommendationService
from services.data_collection_service import DataCollectionService

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
gemini_service = GeminiService()
blip_service = BLIPService()  # This will be lazy loaded
recommendation_service = SimpleRecommendationService()
data_collection_service = DataCollectionService()

def init_blip_service():
    """Initialize BLIP service lazily"""
    global blip_service
    if blip_service is None:
        logger.info("Initializing BLIP service...")
        blip_service = BLIPService()
    return blip_service

def handle_error(e):
    """Handle API errors consistently"""
    logger.error(f"API Error: {str(e)}")
    logger.error(traceback.format_exc())
    return jsonify({
        "error": str(e),
        "timestamp": datetime.utcnow().isoformat(),
        "success": False
    }), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "gemini": "ready",
            "blip": "lazy_loaded",
            "recommendations": "ready"
        }
    })

# ==================== GEMINI AI ENDPOINTS ====================

@app.route('/api/generate-description', methods=['POST'])
def generate_product_description():
    """Generate product description using Gemini AI"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        features = data.get('features', [])
        category = data.get('category')
        image_description = data.get('image_description')
        
        if not product_name:
            return jsonify({"error": "product_name is required"}), 400
        
        result = gemini_service.generate_product_description(
            product_name=product_name,
            features=features,
            category=category,
            image_description=image_description
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/generate-categories', methods=['POST'])
def generate_categories_and_tags():
    """Generate categories and tags using Gemini AI"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        description = data.get('description')
        image_description = data.get('image_description')
        
        if not product_name:
            return jsonify({"error": "product_name is required"}), 400
        
        result = gemini_service.generate_categories_and_tags(
            product_name=product_name,
            description=description,
            image_description=image_description
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/generate-seo', methods=['POST'])
def generate_seo_metadata():
    """Generate SEO metadata using Gemini AI"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        description = data.get('description')
        category = data.get('category')
        price = data.get('price')
        
        if not product_name:
            return jsonify({"error": "product_name is required"}), 400
        
        result = gemini_service.generate_seo_metadata(
            product_name=product_name,
            description=description,
            category=category,
            price=price
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/generate-blog', methods=['POST'])
def generate_blog_content():
    """Generate blog/article content using Gemini AI"""
    try:
        data = request.get_json()
        topic = data.get('topic')
        products = data.get('products', [])
        target_audience = data.get('target_audience')
        content_type = data.get('content_type', 'article')
        
        if not topic:
            return jsonify({"error": "topic is required"}), 400
        
        result = gemini_service.generate_blog_content(
            topic=topic,
            products=products,
            target_audience=target_audience,
            content_type=content_type
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/generate-pricing', methods=['POST'])
def generate_pricing_strategy():
    """Generate pricing strategy using Gemini AI"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        category = data.get('category')
        current_price = data.get('current_price')
        competitor_prices = data.get('competitor_prices', [])
        demand_level = data.get('demand_level', 'medium')
        
        if not all([product_name, category, current_price]):
            return jsonify({"error": "product_name, category, and current_price are required"}), 400
        
        result = gemini_service.generate_pricing_strategy(
            product_name=product_name,
            category=category,
            current_price=current_price,
            competitor_prices=competitor_prices,
            demand_level=demand_level
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/generate-forecast', methods=['POST'])
def generate_sales_forecast():
    """Generate sales forecast using Gemini AI"""
    try:
        data = request.get_json()
        product_data = data.get('product_data')
        historical_data = data.get('historical_data', [])
        
        if not product_data:
            return jsonify({"error": "product_data is required"}), 400
        
        result = gemini_service.generate_sales_forecast(
            product_data=product_data,
            historical_data=historical_data
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

# ==================== BLIP IMAGE ANALYSIS ENDPOINTS ====================

@app.route('/api/analyze-image', methods=['POST'])
def analyze_product_image():
    """Analyze product image using BLIP model"""
    try:
        blip = init_blip_service()
        data = request.get_json()
        
        image_source = data.get('image_source')
        source_type = data.get('source_type', 'url')  # url, path, base64
        
        if not image_source:
            return jsonify({"error": "image_source is required"}), 400
        
        result = blip.analyze_product_image(
            image_source=image_source,
            source_type=source_type
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/generate-alt-text', methods=['POST'])
def generate_alt_text():
    """Generate SEO-friendly alt text for images"""
    try:
        blip = init_blip_service()
        data = request.get_json()
        
        image_source = data.get('image_source')
        source_type = data.get('source_type', 'url')
        product_name = data.get('product_name')
        
        if not image_source:
            return jsonify({"error": "image_source is required"}), 400
        
        result = blip.generate_alt_text(
            image_source=image_source,
            source_type=source_type,
            product_name=product_name
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/batch-analyze-images', methods=['POST'])
def batch_analyze_images():
    """Analyze multiple images in batch"""
    try:
        blip = init_blip_service()
        data = request.get_json()
        
        image_batch = data.get('images', [])
        
        if not image_batch:
            return jsonify({"error": "images array is required"}), 400
        
        result = blip.batch_analyze_images(image_batch)
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

# ==================== RECOMMENDATION ENDPOINTS ====================

@app.route('/api/train-recommendations', methods=['POST'])
def train_recommendation_model():
    """Train recommendation model with data"""
    try:
        data = request.get_json()
        use_sample_data = data.get('use_sample_data', True)
        algorithm = data.get('algorithm', 'NMF')
        ratings_data = data.get('ratings_data')
        
        if use_sample_data:
            # Use generated sample data
            ratings_df = recommendation_service.load_sample_data()
        elif ratings_data:
            # Use provided data
            import pandas as pd
            ratings_df = pd.DataFrame(ratings_data)
        else:
            return jsonify({"error": "Either use_sample_data=True or provide ratings_data"}), 400
        
        # Prepare and train model
        recommendation_service.prepare_data(ratings_df)
        result = recommendation_service.train_model(algorithm=algorithm)
        
        # Save model
        save_result = recommendation_service.save_model()
        result['model_saved'] = save_result
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/user-recommendations/<user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """Get personalized recommendations for a user"""
    try:
        n_recommendations = request.args.get('n_recommendations', 10, type=int)
        exclude_rated = request.args.get('exclude_rated', 'true').lower() == 'true'
        
        # Try to load model if not already loaded
        if recommendation_service.model is None:
            load_result = recommendation_service.load_model()
            if "error" in load_result:
                return jsonify({
                    "error": "Recommendation model not found. Train a model first.",
                    "details": load_result
                }), 404
        
        result = recommendation_service.get_user_recommendations(
            user_id=user_id,
            n_recommendations=n_recommendations,
            exclude_rated=exclude_rated
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/item-recommendations/<item_id>', methods=['GET'])
def get_item_recommendations(item_id):
    """Get similar item recommendations"""
    try:
        n_recommendations = request.args.get('n_recommendations', 10, type=int)
        
        # Try to load model if not already loaded
        if recommendation_service.model is None:
            load_result = recommendation_service.load_model()
            if "error" in load_result:
                return jsonify({
                    "error": "Recommendation model not found. Train a model first.",
                    "details": load_result
                }), 404
        
        result = recommendation_service.get_item_recommendations(
            item_id=item_id,
            n_recommendations=n_recommendations
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/popular-items', methods=['GET'])
def get_popular_items():
    """Get most popular items"""
    try:
        n_items = request.args.get('n_items', 10, type=int)
        min_ratings = request.args.get('min_ratings', 5, type=int)
        
        # Try to load model if not already loaded
        if recommendation_service.model is None:
            load_result = recommendation_service.load_model()
            if "error" in load_result:
                return jsonify({
                    "error": "Recommendation model not found. Train a model first.",
                    "details": load_result
                }), 404
        
        result = recommendation_service.get_popular_items(
            n_items=n_items,
            min_ratings=min_ratings
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/predict-rating', methods=['POST'])
def predict_rating():
    """Predict rating for user-item pair"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        
        if not all([user_id, item_id]):
            return jsonify({"error": "user_id and item_id are required"}), 400
        
        # Try to load model if not already loaded
        if recommendation_service.model is None:
            load_result = recommendation_service.load_model()
            if "error" in load_result:
                return jsonify({
                    "error": "Recommendation model not found. Train a model first.",
                    "details": load_result
                }), 404
        
        result = recommendation_service.predict_rating(
            user_id=user_id,
            item_id=item_id
        )
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/model-stats', methods=['GET'])
def get_model_stats():
    """Get recommendation model statistics"""
    try:
        # Try to load model if not already loaded
        if recommendation_service.model is None:
            load_result = recommendation_service.load_model()
            if "error" in load_result:
                return jsonify({
                    "error": "Recommendation model not found. Train a model first.",
                    "details": load_result
                }), 404
        
        result = recommendation_service.get_model_stats()
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

# ==================== DATA COLLECTION ENDPOINTS ====================

@app.route('/api/track-interaction', methods=['POST'])
def track_user_interaction():
    """Track user interaction with products"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        interaction_type = data.get('interaction_type')
        interaction_value = data.get('interaction_value')
        session_id = data.get('session_id')
        metadata = data.get('metadata')
        
        if not all([user_id, product_id, interaction_type]):
            return jsonify({"error": "user_id, product_id, and interaction_type are required"}), 400
        
        success = data_collection_service.track_user_interaction(
            user_id=user_id,
            product_id=product_id,
            interaction_type=interaction_type,
            interaction_value=interaction_value,
            session_id=session_id,
            metadata=metadata
        )
        
        return jsonify({
            "success": success,
            "message": "Interaction tracked successfully" if success else "Failed to track interaction",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/track-view', methods=['POST'])
def track_product_view():
    """Track product page view"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        user_id = data.get('user_id')
        view_duration = data.get('view_duration')
        referrer = data.get('referrer')
        user_agent = data.get('user_agent')
        
        if not product_id:
            return jsonify({"error": "product_id is required"}), 400
        
        success = data_collection_service.track_product_view(
            product_id=product_id,
            user_id=user_id,
            view_duration=view_duration,
            referrer=referrer,
            user_agent=user_agent
        )
        
        return jsonify({
            "success": success,
            "message": "View tracked successfully" if success else "Failed to track view",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/track-purchase', methods=['POST'])
def track_purchase():
    """Track product purchase"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        price = data.get('price', 0)
        order_id = data.get('order_id')
        
        if not all([user_id, product_id]):
            return jsonify({"error": "user_id and product_id are required"}), 400
        
        success = data_collection_service.track_purchase(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
            order_id=order_id
        )
        
        return jsonify({
            "success": success,
            "message": "Purchase tracked successfully" if success else "Failed to track purchase",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/track-rating', methods=['POST'])
def track_product_rating():
    """Track product rating and review"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        rating = data.get('rating')
        review_text = data.get('review_text')
        
        if not all([user_id, product_id, rating]):
            return jsonify({"error": "user_id, product_id, and rating are required"}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({"error": "rating must be between 1 and 5"}), 400
        
        success = data_collection_service.track_rating(
            user_id=user_id,
            product_id=product_id,
            rating=rating,
            review_text=review_text
        )
        
        return jsonify({
            "success": success,
            "message": "Rating tracked successfully" if success else "Failed to track rating",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/track-search', methods=['POST'])
def track_search_query():
    """Track search query"""
    try:
        data = request.get_json()
        query = data.get('query')
        user_id = data.get('user_id')
        results_count = data.get('results_count')
        clicked_results = data.get('clicked_results')
        
        if not query:
            return jsonify({"error": "query is required"}), 400
        
        success = data_collection_service.track_search_query(
            query=query,
            user_id=user_id,
            results_count=results_count,
            clicked_results=clicked_results
        )
        
        return jsonify({
            "success": success,
            "message": "Search tracked successfully" if success else "Failed to track search",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/track-ai-performance', methods=['POST'])
def track_ai_content_performance():
    """Track performance of AI-generated content"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        content_type = data.get('content_type')
        generated_content = data.get('generated_content')
        performance_metrics = data.get('performance_metrics')
        
        if not all([product_id, content_type, generated_content]):
            return jsonify({"error": "product_id, content_type, and generated_content are required"}), 400
        
        success = data_collection_service.track_ai_content_performance(
            product_id=product_id,
            content_type=content_type,
            generated_content=generated_content,
            performance_metrics=performance_metrics
        )
        
        return jsonify({
            "success": success,
            "message": "AI content performance tracked successfully" if success else "Failed to track AI content performance",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/data/user-history/<user_id>', methods=['GET'])
def get_user_interaction_history(user_id):
    """Get user interaction history"""
    try:
        days_back = request.args.get('days_back', 30, type=int)
        
        df = data_collection_service.get_user_interaction_history(user_id, days_back)
        
        return jsonify({
            "success": True,
            "data": {
                "user_id": user_id,
                "days_back": days_back,
                "interactions": df.to_dict('records')
            },
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/data/popularity-metrics', methods=['GET'])
def get_popularity_metrics():
    """Get product popularity metrics"""
    try:
        metrics = data_collection_service.get_product_popularity_metrics()
        
        return jsonify({
            "success": True,
            "data": metrics,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/data/user-insights', methods=['GET'])
def get_user_behavior_insights():
    """Get user behavior insights"""
    try:
        insights = data_collection_service.get_user_behavior_insights()
        
        return jsonify({
            "success": True,
            "data": insights,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/data/collection-stats', methods=['GET'])
def get_data_collection_stats():
    """Get statistics about collected data"""
    try:
        stats = data_collection_service.get_data_collection_stats()
        
        return jsonify({
            "success": True,
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/data/export', methods=['POST'])
def export_training_data():
    """Export collected data for AI model training"""
    try:
        data = request.get_json()
        output_dir = data.get('output_dir', 'training_data')
        
        exported_files = data_collection_service.export_data_for_training(output_dir)
        
        return jsonify({
            "success": True,
            "data": {
                "exported_files": exported_files,
                "output_directory": output_dir
            },
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

@app.route('/api/data/ratings-for-ml', methods=['GET'])
def get_ratings_for_ml():
    """Get ratings data formatted for machine learning"""
    try:
        df = data_collection_service.get_ratings_data_for_ml()
        
        return jsonify({
            "success": True,
            "data": {
                "ratings_count": len(df),
                "unique_users": df['user_id'].nunique() if not df.empty else 0,
                "unique_products": df['product_id'].nunique() if not df.empty else 0,
                "ratings_data": df.to_dict('records')
            },
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

# ==================== COMBINED AUTOMATION ENDPOINTS ====================

@app.route('/api/complete-product-automation', methods=['POST'])
def complete_product_automation():
    """Complete product automation pipeline"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        features = data.get('features', [])
        category = data.get('category')
        price = data.get('price')
        image_source = data.get('image_source')
        source_type = data.get('source_type', 'url')
        
        if not product_name:
            return jsonify({"error": "product_name is required"}), 400
        
        results = {}
        
        # 1. Image Analysis (if image provided)
        image_description = None
        if image_source:
            blip = init_blip_service()
            image_result = blip.analyze_product_image(image_source, source_type)
            results['image_analysis'] = image_result
            
            if 'analysis' in image_result:
                image_description = image_result['analysis'].get('product_description', '')
        
        # 2. Generate Description
        description_result = gemini_service.generate_product_description(
            product_name=product_name,
            features=features,
            category=category,
            image_description=image_description
        )
        results['description'] = description_result
        
        # 3. Generate Categories and Tags
        categories_result = gemini_service.generate_categories_and_tags(
            product_name=product_name,
            description=description_result.get('description'),
            image_description=image_description
        )
        results['categories_tags'] = categories_result
        
        # 4. Generate SEO Metadata
        seo_result = gemini_service.generate_seo_metadata(
            product_name=product_name,
            description=description_result.get('description'),
            category=category,
            price=price
        )
        results['seo_metadata'] = seo_result
        
        # 5. Generate Alt Text (if image provided)
        if image_source:
            alt_text_result = blip.generate_alt_text(
                image_source=image_source,
                source_type=source_type,
                product_name=product_name
            )
            results['alt_text'] = alt_text_result
        
        return jsonify({
            "success": True,
            "data": results,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return handle_error(e)

# ==================== MAIN APPLICATION ====================

if __name__ == '__main__':
    logger.info("Starting AI Automation System...")
    logger.info(f"Configuration: {Config.__dict__}")
    
    # Initialize sample recommendation model if needed
    if not os.path.exists("simple_recommendation_model.pkl"):
        logger.info("No recommendation model found. You can train one using /api/train-recommendations")
    
    app.run(
        host='0.0.0.0',
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )
