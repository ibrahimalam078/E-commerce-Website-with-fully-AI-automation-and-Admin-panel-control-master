# AI-Powered E-Commerce Automation System

A comprehensive automation system for e-commerce admin panels powered by Google Gemini 2.0 Flash API, Hugging Face BLIP, and scikit-learn recommendation engine.

## 🚀 Features

### 1. **Product Content Generation** (Gemini AI)
- **Product Descriptions**: Generate compelling, SEO-optimized product descriptions
- **Categories & Tags**: Automatically categorize products and generate relevant tags
- **SEO Metadata**: Create meta titles, descriptions, and keywords for better search visibility
- **Blog Content**: Generate educational content and articles related to products
- **Pricing Strategies**: AI-powered pricing recommendations based on market analysis
- **Sales Forecasting**: Predict sales trends and performance metrics

### 2. **Image Analysis** (BLIP Model)
- **Product Image Captioning**: Automatically describe product images
- **SEO Alt Text**: Generate SEO-friendly alt text for images
- **Batch Processing**: Analyze multiple images simultaneously
- **Multi-format Support**: Handle URLs, local files, and base64 images

### 3. **Recommendation System** (scikit-learn)
- **Personalized Recommendations**: User-based collaborative filtering
- **Similar Products**: Find and suggest related items
- **Popular Items**: Track and display trending products
- **Rating Prediction**: Predict user preferences for products
- **Cold Start Handling**: Recommendations for new users and items

## 📁 Project Structure

```
ai_automation/
├── services/
│   ├── gemini_service.py          # Google Gemini AI integration
│   ├── blip_service.py           # Hugging Face BLIP model
│   ├── simple_recommendation_service.py  # Recommendation engine
│   └── __init__.py
├── scripts/
│   ├── test_gemini.py            # Individual Gemini tests
│   ├── test_blip.py              # Individual BLIP tests
│   ├── test_recommendations.py   # Individual recommendation tests
│   └── api_examples.py          # Full API usage examples
├── app.py                        # Flask API server
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
├── manual_test.py               # Manual recommendation test
├── test_api.py                  # Complete API test suite
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Virtual environment (recommended)

### Step 1: Clone and Setup Virtual Environment
```bash
# Create project directory
mkdir ai_automation
cd ai_automation

# Create virtual environment
python -m venv ai_env

# Activate virtual environment
# Windows:
ai_env\Scripts\activate
# Mac/Linux:
source ai_env/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration
Create a `.env` file in the project root:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Hugging Face token (for higher rate limits)
HUGGINGFACE_API_TOKEN=your_huggingface_token_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# Database (currently using SQLite)
DATABASE_URL=sqlite:///ecommerce.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=automation.log

# AI Model Settings
MAX_TOKENS=1000
TEMPERATURE=0.7

# Recommendation Settings
MIN_RATINGS=5
N_RECOMMENDATIONS=10
```

### Step 4: Get Your Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 🚀 Usage

### Starting the Server
```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

### Running Tests

#### Manual Recommendation Test
```bash
python manual_test.py
```

#### Complete API Test Suite
```bash
# Start the server first in another terminal:
python app.py

# Then run tests:
python test_api.py
```

## 📚 API Documentation

### Health Check
```http
GET /health
```

### Product Content Generation

#### Generate Product Description
```http
POST /api/generate-description
Content-Type: application/json

{
    "product_name": "Organic Turmeric Essential Oil",
    "features": ["100% pure", "organic", "anti-inflammatory"],
    "category": "Essential Oils",
    "image_description": "Golden yellow essential oil in glass bottle"
}
```

#### Generate Categories and Tags
```http
POST /api/generate-categories
Content-Type: application/json

{
    "product_name": "Lavender Essential Oil",
    "description": "Pure lavender oil for aromatherapy",
    "image_description": "Purple flowers in background"
}
```

#### Generate SEO Metadata
```http
POST /api/generate-seo
Content-Type: application/json

{
    "product_name": "Tea Tree Oil",
    "description": "Natural antiseptic essential oil",
    "category": "Essential Oils",
    "price": 19.99
}
```

### Image Analysis

#### Analyze Product Image
```http
POST /api/analyze-image
Content-Type: application/json

{
    "image_source": "https://example.com/product.jpg",
    "source_type": "url"
}
```

#### Generate Alt Text
```http
POST /api/generate-alt-text
Content-Type: application/json

{
    "image_source": "https://example.com/product.jpg",
    "source_type": "url",
    "product_name": "Lavender Oil"
}
```

### Recommendation System

#### Train Recommendation Model
```http
POST /api/train-recommendations
Content-Type: application/json

{
    "use_sample_data": true,
    "algorithm": "NMF"
}
```

#### Get User Recommendations
```http
GET /api/user-recommendations/user_5?n_recommendations=10&exclude_rated=true
```

#### Get Similar Products
```http
GET /api/item-recommendations/Turmeric%20CO2%20Extract?n_recommendations=5
```

#### Get Popular Items
```http
GET /api/popular-items?n_items=10&min_ratings=5
```

#### Predict Rating
```http
POST /api/predict-rating
Content-Type: application/json

{
    "user_id": "user_10",
    "item_id": "Lavender Oil"
}
```

### Combined Automation
```http
POST /api/complete-product-automation
Content-Type: application/json

{
    "product_name": "Organic Rose Oil",
    "features": ["100% pure", "organic", "premium"],
    "category": "Essential Oils",
    "price": 49.99,
    "image_source": "https://example.com/rose-oil.jpg",
    "source_type": "url"
}
```

## 💡 Example Use Cases

### 1. New Product Launch
```python
import requests

# Complete product automation pipeline
payload = {
    "product_name": "Himalayan Pink Salt Scrub",
    "features": ["Exfoliating", "Natural", "Moisturizing", "Detoxifying"],
    "category": "Body Care",
    "price": 24.99,
    "image_source": "https://example.com/salt-scrub.jpg"
}

response = requests.post(
    "http://127.0.0.1:5000/api/complete-product-automation",
    json=payload
)

result = response.json()
# Contains: description, categories, SEO metadata, image analysis, alt text
```

### 2. User Personalization
```python
# Get personalized recommendations for a user
user_id = "user_123"
response = requests.get(
    f"http://127.0.0.1:5000/api/user-recommendations/{user_id}?n_recommendations=5"
)

recommendations = response.json()['data']['recommendations']
for rec in recommendations:
    print(f"Recommend: {rec['product_id']} (rating: {rec['predicted_rating']:.2f})")
```

### 3. Content Marketing
```python
# Generate blog content
payload = {
    "topic": "Benefits of Essential Oils for Wellness",
    "products": ["Lavender Oil", "Tea Tree Oil", "Eucalyptus Oil"],
    "target_audience": "Health-conscious consumers",
    "content_type": "blog_post"
}

response = requests.post(
    "http://127.0.0.1:5000/api/generate-blog",
    json=payload
)

blog_content = response.json()['data']
```

## 🔧 System Architecture

### Service Layer Architecture
- **GeminiService**: Handles all AI text generation tasks
- **BLIPService**: Manages image analysis and captioning  
- **SimpleRecommendationService**: Provides collaborative filtering recommendations

### API Design
- RESTful endpoints with consistent JSON responses
- Error handling with detailed error messages
- Request validation and parameter checking
- CORS support for web integration

### Data Flow
1. **Input**: Product data, user preferences, images
2. **Processing**: AI models analyze and generate content
3. **Output**: Structured JSON responses with generated content
4. **Storage**: Model persistence for recommendations

## 📊 Sample Data

The recommendation system includes sample e-commerce data:
- **100 users** with diverse rating patterns
- **30 natural products** (essential oils, extracts, supplements)
- **1,497 ratings** with realistic distribution
- **Bias towards popular items** (Turmeric, Lavender Oil, Tea Tree Oil)

## 🎯 Performance

### Recommendation System
- **Algorithm**: Non-negative Matrix Factorization (NMF)
- **Training Time**: ~2-3 seconds for sample dataset
- **Prediction Time**: <50ms per recommendation
- **Memory Usage**: ~10MB for trained model
- **Accuracy**: Collaborative filtering with cosine similarity

### AI Services
- **Gemini API**: ~2-5 seconds response time
- **BLIP Model**: ~1-3 seconds per image
- **Batch Processing**: Supported for multiple images

## 🔒 Security Considerations

- API keys stored in environment variables
- Input validation and sanitization
- Rate limiting considerations for AI APIs
- HTTPS recommended for production
- CORS configuration for web integration

## 🚀 Production Deployment

### Recommendations for Production:
1. **Use a production WSGI server** (Gunicorn, uWSGI)
2. **Set up load balancing** for high availability
3. **Use Redis** for caching recommendations
4. **Implement proper logging** and monitoring
5. **Set up database** (PostgreSQL, MySQL) instead of SQLite
6. **Configure SSL/HTTPS**
7. **Set up CI/CD pipeline**

### Example Production Configuration:
```bash
# Install production dependencies
pip install gunicorn redis

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🛠️ Customization

### Adding New AI Features
1. Extend `GeminiService` with new methods
2. Add corresponding Flask routes in `app.py`
3. Update test scripts

### Custom Recommendation Algorithms
1. Modify `SimpleRecommendationService`
2. Add new algorithms to `train_model()` method
3. Update model evaluation metrics

### Integration with Existing Systems
- REST API can be integrated with any web framework
- JSON responses are compatible with most frontend technologies
- Database models can be adapted to existing schemas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For questions, issues, or feature requests:
1. Check the test scripts for usage examples
2. Review the API documentation above
3. Examine the service implementations for customization options

## 📈 Roadmap

- [ ] Integration with more AI models (OpenAI GPT, Claude)
- [ ] Advanced recommendation algorithms (Deep Learning)
- [ ] Real-time analytics dashboard
- [ ] A/B testing framework for recommendations
- [ ] Multi-language support
- [ ] Advanced image analysis features
- [ ] Integration with popular e-commerce platforms

---

**Ready to automate your e-commerce operations with AI? Start the server and begin exploring the powerful automation features!** 🚀
