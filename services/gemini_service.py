"""
Google Gemini AI Service
Handles all interactions with Google Gemini 2.0 Flash API
"""
import google.generativeai as genai
import logging
from typing import Dict, List, Optional, Any
from config import Config

logger = logging.getLogger(__name__)

class GeminiService:
    """Service class for Google Gemini AI operations"""
    
    def __init__(self):
        """Initialize Gemini service"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def generate_product_description(self, product_name: str, features: List[str] = None, 
                                   category: str = None, image_description: str = None) -> Dict[str, Any]:
        """
        Generate compelling product description
        
        Args:
            product_name: Name of the product
            features: List of product features
            category: Product category
            image_description: Description from image analysis
            
        Returns:
            Dict containing generated description and metadata
        """
        try:
            features_text = ", ".join(features) if features else "high-quality product"
            category_text = f" in {category}" if category else ""
            image_context = f"Based on image analysis: {image_description}. " if image_description else ""
            
            prompt = f"""
            Create a compelling, SEO-optimized product description for an e-commerce store.
            
            Product: {product_name}
            Category: {category_text}
            Features: {features_text}
            {image_context}
            
            Requirements:
            - Write 2-3 engaging paragraphs
            - Include key benefits and features
            - Use persuasive, customer-focused language
            - Include relevant keywords naturally
            - End with a call-to-action
            - Target length: 150-250 words
            
            Format the response as JSON with keys: description, key_features, benefits, call_to_action
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse JSON response or format as needed
            result = {
                "description": response.text,
                "generated_at": "2025-08-14T19:18:38Z",
                "model": "gemini-2.0-flash-exp"
            }
            
            logger.info(f"Generated product description for: {product_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating product description: {str(e)}")
            return {"error": str(e)}
    
    def generate_categories_and_tags(self, product_name: str, description: str = None, 
                                   image_description: str = None) -> Dict[str, Any]:
        """
        Generate product categories and tags
        
        Args:
            product_name: Name of the product
            description: Product description
            image_description: Description from image analysis
            
        Returns:
            Dict containing categories and tags
        """
        try:
            desc_context = f"Description: {description}. " if description else ""
            image_context = f"Image shows: {image_description}. " if image_description else ""
            
            prompt = f"""
            Analyze the following product and suggest appropriate categories and tags for an e-commerce store.
            
            Product: {product_name}
            {desc_context}
            {image_context}
            
            Provide:
            1. Primary category (most specific)
            2. Secondary category (broader)
            3. Department (top-level)
            4. 8-10 relevant tags for search and filtering
            5. Target audience
            6. Use cases
            
            Consider: Health & Wellness, Beauty & Personal Care, Natural Products, Essential Oils, Supplements, etc.
            
            Format as JSON with keys: primary_category, secondary_category, department, tags, target_audience, use_cases
            """
            
            response = self.model.generate_content(prompt)
            
            result = {
                "classification": response.text,
                "generated_at": "2025-08-14T19:18:38Z",
                "model": "gemini-2.0-flash-exp"
            }
            
            logger.info(f"Generated categories and tags for: {product_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating categories and tags: {str(e)}")
            return {"error": str(e)}
    
    def generate_seo_metadata(self, product_name: str, description: str = None, 
                            category: str = None, price: float = None) -> Dict[str, Any]:
        """
        Generate SEO metadata (title, description, keywords)
        
        Args:
            product_name: Name of the product
            description: Product description
            category: Product category
            price: Product price
            
        Returns:
            Dict containing SEO metadata
        """
        try:
            desc_context = f"Description: {description}. " if description else ""
            category_context = f"Category: {category}. " if category else ""
            price_context = f"Price: ${price}. " if price else ""
            
            prompt = f"""
            Generate SEO-optimized metadata for this product page.
            
            Product: {product_name}
            {desc_context}
            {category_context}
            {price_context}
            
            Generate:
            1. SEO Title (50-60 characters, includes primary keyword)
            2. Meta Description (150-160 characters, compelling and descriptive)
            3. 10-15 relevant keywords (mix of short and long-tail)
            4. URL slug (SEO-friendly)
            5. Alt text for main product image
            6. Open Graph title and description
            
            Focus on natural products, wellness, and e-commerce keywords.
            
            Format as JSON with keys: seo_title, meta_description, keywords, url_slug, alt_text, og_title, og_description
            """
            
            response = self.model.generate_content(prompt)
            
            result = {
                "seo_metadata": response.text,
                "generated_at": "2025-08-14T19:18:38Z",
                "model": "gemini-2.0-flash-exp"
            }
            
            logger.info(f"Generated SEO metadata for: {product_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating SEO metadata: {str(e)}")
            return {"error": str(e)}
    
    def generate_blog_content(self, topic: str, products: List[str] = None, 
                            target_audience: str = None, content_type: str = "article") -> Dict[str, Any]:
        """
        Generate blog/article content for marketing
        
        Args:
            topic: Main topic or theme
            products: List of products to feature
            target_audience: Target audience description
            content_type: Type of content (article, guide, review, etc.)
            
        Returns:
            Dict containing blog content
        """
        try:
            products_context = f"Feature these products: {', '.join(products)}. " if products else ""
            audience_context = f"Target audience: {target_audience}. " if target_audience else "health-conscious consumers"
            
            prompt = f"""
            Write a comprehensive {content_type} about "{topic}" for a natural health and wellness e-commerce blog.
            
            Requirements:
            - Target audience: {audience_context}
            - {products_context}
            - Length: 800-1200 words
            - Include: Introduction, main content with subheadings, conclusion
            - SEO-optimized with natural keyword placement
            - Engaging, informative, and trustworthy tone
            - Include call-to-action
            - Add relevant FAQs at the end
            
            Structure:
            1. Compelling headline
            2. Meta description
            3. Introduction (hook the reader)
            4. Main content with 3-4 subheadings
            5. Conclusion with CTA
            6. 3-5 FAQs
            
            Format as JSON with keys: headline, meta_description, introduction, main_content, conclusion, faqs, tags
            """
            
            response = self.model.generate_content(prompt)
            
            result = {
                "blog_content": response.text,
                "topic": topic,
                "content_type": content_type,
                "generated_at": "2025-08-14T19:18:38Z",
                "model": "gemini-2.0-flash-exp"
            }
            
            logger.info(f"Generated {content_type} content for topic: {topic}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating blog content: {str(e)}")
            return {"error": str(e)}
    
    def generate_pricing_strategy(self, product_name: str, category: str, 
                                current_price: float, competitor_prices: List[float] = None,
                                demand_level: str = "medium") -> Dict[str, Any]:
        """
        Generate dynamic pricing suggestions
        
        Args:
            product_name: Name of the product
            category: Product category
            current_price: Current product price
            competitor_prices: List of competitor prices
            demand_level: Current demand level (low, medium, high)
            
        Returns:
            Dict containing pricing recommendations
        """
        try:
            competitor_context = ""
            if competitor_prices:
                avg_competitor = sum(competitor_prices) / len(competitor_prices)
                competitor_context = f"Competitor prices: {competitor_prices}, Average: ${avg_competitor:.2f}. "
            
            prompt = f"""
            Analyze and recommend pricing strategy for this product.
            
            Product: {product_name}
            Category: {category}
            Current Price: ${current_price}
            {competitor_context}
            Current Demand: {demand_level}
            
            Consider:
            - Market positioning
            - Competition analysis
            - Demand trends
            - Price elasticity
            - Profit margins
            - Psychological pricing
            
            Provide:
            1. Recommended price range
            2. Optimal price point
            3. Pricing strategy explanation
            4. Expected impact on sales
            5. Alternative pricing tactics
            6. Seasonal considerations
            
            Format as JSON with keys: recommended_price, price_range, strategy, expected_impact, alternatives, notes
            """
            
            response = self.model.generate_content(prompt)
            
            result = {
                "pricing_analysis": response.text,
                "current_price": current_price,
                "demand_level": demand_level,
                "generated_at": "2025-08-14T19:18:38Z",
                "model": "gemini-2.0-flash-exp"
            }
            
            logger.info(f"Generated pricing strategy for: {product_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating pricing strategy: {str(e)}")
            return {"error": str(e)}
    
    def generate_sales_forecast(self, product_data: Dict[str, Any], 
                              historical_data: List[Dict] = None) -> Dict[str, Any]:
        """
        Generate sales forecasting analysis
        
        Args:
            product_data: Current product information
            historical_data: Historical sales data
            
        Returns:
            Dict containing sales forecast
        """
        try:
            historical_context = ""
            if historical_data:
                historical_context = f"Historical sales data: {historical_data[:5]}... "  # Limit for context
            
            prompt = f"""
            Generate sales forecast and inventory recommendations.
            
            Product Information: {product_data}
            {historical_context}
            
            Analyze and predict:
            1. Sales forecast for next 30, 60, 90 days
            2. Seasonal trends and patterns
            3. Inventory recommendations
            4. Reorder points and quantities
            5. Risk factors and mitigation
            6. Market opportunities
            
            Consider:
            - Seasonal variations
            - Market trends
            - Product lifecycle
            - Economic factors
            - Competition
            
            Format as JSON with keys: forecast_30d, forecast_60d, forecast_90d, inventory_recommendations, risk_factors, opportunities
            """
            
            response = self.model.generate_content(prompt)
            
            result = {
                "sales_forecast": response.text,
                "product_data": product_data,
                "generated_at": "2025-08-14T19:18:38Z",
                "model": "gemini-2.0-flash-exp"
            }
            
            logger.info(f"Generated sales forecast for: {product_data.get('name', 'product')}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating sales forecast: {str(e)}")
            return {"error": str(e)}
