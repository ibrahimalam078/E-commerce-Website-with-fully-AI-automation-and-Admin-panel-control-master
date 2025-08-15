#!/usr/bin/env python3
"""
Test script for Gemini AI features
Run individual Gemini AI automation features
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gemini_service import GeminiService
import json
import argparse

def test_product_description():
    """Test product description generation"""
    print("🔍 Testing Product Description Generation...")
    
    service = GeminiService()
    
    test_cases = [
        {
            "product_name": "Organic Turmeric CO2 Extract",
            "features": ["Anti-inflammatory", "High curcumin content", "CO2 extracted", "Organic certified"],
            "category": "Natural Extracts",
            "image_description": "Golden yellow powder in a glass jar with organic certification label"
        },
        {
            "product_name": "Pure Lavender Essential Oil",
            "features": ["Calming", "Sleep aid", "100% pure", "Steam distilled"],
            "category": "Essential Oils"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['product_name']}")
        result = service.generate_product_description(**test_case)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Generated description:")
            print(f"📄 {result['description'][:200]}...")
            print(f"🔧 Model: {result.get('model', 'Unknown')}")

def test_categories_and_tags():
    """Test category and tag generation"""
    print("\n🏷️ Testing Categories and Tags Generation...")
    
    service = GeminiService()
    
    test_cases = [
        {
            "product_name": "Organic Ashwagandha Root Extract",
            "description": "Premium quality ashwagandha root extract for stress relief and energy boost",
            "image_description": "Brown powder in capsules"
        },
        {
            "product_name": "Pure Clove Essential Oil",
            "description": "Antiseptic and aromatic clove oil for dental care and aromatherapy"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['product_name']}")
        result = service.generate_categories_and_tags(**test_case)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Generated classification:")
            print(f"📄 {result['classification'][:300]}...")

def test_seo_metadata():
    """Test SEO metadata generation"""
    print("\n🔍 Testing SEO Metadata Generation...")
    
    service = GeminiService()
    
    test_cases = [
        {
            "product_name": "Premium Argan Oil for Hair and Skin",
            "description": "Cold-pressed, organic argan oil rich in vitamin E and essential fatty acids",
            "category": "Beauty Oils",
            "price": 29.99
        },
        {
            "product_name": "Natural Honey Manuka UMF 15+",
            "description": "Authentic New Zealand Manuka honey with verified UMF rating",
            "category": "Natural Sweeteners",
            "price": 45.99
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['product_name']}")
        result = service.generate_seo_metadata(**test_case)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Generated SEO metadata:")
            print(f"📄 {result['seo_metadata'][:300]}...")

def test_blog_content():
    """Test blog content generation"""
    print("\n📰 Testing Blog Content Generation...")
    
    service = GeminiService()
    
    test_cases = [
        {
            "topic": "Benefits of Essential Oils for Mental Wellness",
            "products": ["Lavender Oil", "Peppermint Oil", "Eucalyptus Oil"],
            "target_audience": "wellness enthusiasts and aromatherapy beginners",
            "content_type": "guide"
        },
        {
            "topic": "Natural Skincare Routine with Organic Ingredients",
            "products": ["Argan Oil", "Aloe Vera Gel", "Rose Hip Oil"],
            "target_audience": "people seeking natural beauty solutions",
            "content_type": "article"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['topic']}")
        result = service.generate_blog_content(**test_case)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Generated {test_case['content_type']}:")
            print(f"📄 {result['blog_content'][:400]}...")

def test_pricing_strategy():
    """Test pricing strategy generation"""
    print("\n💰 Testing Pricing Strategy Generation...")
    
    service = GeminiService()
    
    test_cases = [
        {
            "product_name": "Premium CBD Oil 1000mg",
            "category": "CBD Products",
            "current_price": 79.99,
            "competitor_prices": [69.99, 89.99, 84.99, 75.00],
            "demand_level": "high"
        },
        {
            "product_name": "Organic Spirulina Powder",
            "category": "Superfood Supplements",
            "current_price": 24.99,
            "competitor_prices": [19.99, 29.99, 27.50],
            "demand_level": "medium"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['product_name']}")
        result = service.generate_pricing_strategy(**test_case)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Generated pricing strategy:")
            print(f"💵 Current Price: ${test_case['current_price']}")
            print(f"📊 Demand Level: {test_case['demand_level']}")
            print(f"📄 Strategy: {result['pricing_analysis'][:300]}...")

def test_sales_forecast():
    """Test sales forecast generation"""
    print("\n📈 Testing Sales Forecast Generation...")
    
    service = GeminiService()
    
    test_cases = [
        {
            "product_data": {
                "name": "Organic Green Tea Extract",
                "category": "Health Supplements",
                "current_price": 34.99,
                "current_inventory": 150,
                "avg_monthly_sales": 45
            },
            "historical_data": [
                {"month": "2024-01", "sales": 42, "revenue": 1470.58},
                {"month": "2024-02", "sales": 48, "revenue": 1679.52},
                {"month": "2024-03", "sales": 51, "revenue": 1784.49},
                {"month": "2024-04", "sales": 43, "revenue": 1504.57}
            ]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        product_name = test_case["product_data"]["name"]
        print(f"\n📝 Test Case {i}: {product_name}")
        result = service.generate_sales_forecast(**test_case)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Generated sales forecast:")
            print(f"📊 Product: {product_name}")
            print(f"📄 Forecast: {result['sales_forecast'][:300]}...")

def main():
    """Main function to run tests"""
    parser = argparse.ArgumentParser(description='Test Gemini AI Features')
    parser.add_argument('--feature', choices=[
        'description', 'categories', 'seo', 'blog', 'pricing', 'forecast', 'all'
    ], default='all', help='Feature to test')
    
    args = parser.parse_args()
    
    print("🤖 Gemini AI Feature Testing")
    print("=" * 50)
    
    try:
        if args.feature == 'all':
            test_product_description()
            test_categories_and_tags()
            test_seo_metadata()
            test_blog_content()
            test_pricing_strategy()
            test_sales_forecast()
        elif args.feature == 'description':
            test_product_description()
        elif args.feature == 'categories':
            test_categories_and_tags()
        elif args.feature == 'seo':
            test_seo_metadata()
        elif args.feature == 'blog':
            test_blog_content()
        elif args.feature == 'pricing':
            test_pricing_strategy()
        elif args.feature == 'forecast':
            test_sales_forecast()
        
        print("\n✅ Testing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
