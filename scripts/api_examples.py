#!/usr/bin/env python3
"""
API Usage Examples and Testing Script
Demonstrates how to use all API endpoints with real examples
"""
import requests
import json
import time
import sys
import argparse

# API Configuration
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

def check_server_health():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is healthy and running")
            return True
        else:
            print(f"⚠️ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server first:")
        print("   python app.py")
        return False

def print_response(title, response):
    """Print formatted API response"""
    print(f"\n{title}")
    print("=" * len(title))
    print(f"Status: {response.status_code}")
    
    try:
        data = response.json()
        if data.get('success'):
            print("✅ Success")
        else:
            print("❌ Failed")
        
        # Pretty print JSON response (truncated)
        json_str = json.dumps(data, indent=2)
        if len(json_str) > 500:
            json_str = json_str[:500] + "...\n}"
        print("Response:", json_str)
        
    except json.JSONDecodeError:
        print("Response:", response.text[:200])

def test_gemini_features():
    """Test all Gemini AI features"""
    print("\n🤖 TESTING GEMINI AI FEATURES")
    print("=" * 50)
    
    # 1. Product Description Generation
    print_response(
        "1. Product Description Generation",
        requests.post(
            f"{BASE_URL}/api/generate-description",
            headers=HEADERS,
            json={
                "product_name": "Organic Turmeric CO2 Extract",
                "features": ["Anti-inflammatory", "High curcumin content", "CO2 extracted", "Organic certified"],
                "category": "Natural Extracts",
                "image_description": "Golden yellow powder in a glass jar with organic certification label"
            }
        )
    )
    
    # 2. Categories and Tags Generation
    print_response(
        "2. Categories and Tags Generation",
        requests.post(
            f"{BASE_URL}/api/generate-categories",
            headers=HEADERS,
            json={
                "product_name": "Pure Lavender Essential Oil",
                "description": "100% pure lavender essential oil, steam distilled from premium lavender flowers"
            }
        )
    )
    
    # 3. SEO Metadata Generation
    print_response(
        "3. SEO Metadata Generation",
        requests.post(
            f"{BASE_URL}/api/generate-seo",
            headers=HEADERS,
            json={
                "product_name": "Premium Argan Oil for Hair and Skin",
                "description": "Cold-pressed, organic argan oil rich in vitamin E and essential fatty acids",
                "category": "Beauty Oils",
                "price": 29.99
            }
        )
    )
    
    # 4. Blog Content Generation
    print_response(
        "4. Blog Content Generation",
        requests.post(
            f"{BASE_URL}/api/generate-blog",
            headers=HEADERS,
            json={
                "topic": "Benefits of Essential Oils for Mental Wellness",
                "products": ["Lavender Oil", "Peppermint Oil", "Eucalyptus Oil"],
                "target_audience": "wellness enthusiasts and aromatherapy beginners",
                "content_type": "guide"
            }
        )
    )
    
    # 5. Pricing Strategy Generation
    print_response(
        "5. Pricing Strategy Generation",
        requests.post(
            f"{BASE_URL}/api/generate-pricing",
            headers=HEADERS,
            json={
                "product_name": "Premium CBD Oil 1000mg",
                "category": "CBD Products",
                "current_price": 79.99,
                "competitor_prices": [69.99, 89.99, 84.99, 75.00],
                "demand_level": "high"
            }
        )
    )
    
    # 6. Sales Forecast Generation
    print_response(
        "6. Sales Forecast Generation",
        requests.post(
            f"{BASE_URL}/api/generate-forecast",
            headers=HEADERS,
            json={
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
                    {"month": "2024-03", "sales": 51, "revenue": 1784.49}
                ]
            }
        )
    )

def test_image_analysis():
    """Test BLIP image analysis features"""
    print("\n🖼️ TESTING BLIP IMAGE ANALYSIS")
    print("=" * 50)
    
    # Sample image URLs (using Unsplash for free stock images)
    sample_images = {
        "turmeric": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=500",
        "essential_oils": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=500"
    }
    
    # 1. Single Image Analysis
    print_response(
        "1. Single Image Analysis",
        requests.post(
            f"{BASE_URL}/api/analyze-image",
            headers=HEADERS,
            json={
                "image_source": sample_images["turmeric"],
                "source_type": "url"
            }
        )
    )
    
    # 2. Alt Text Generation
    print_response(
        "2. Alt Text Generation",
        requests.post(
            f"{BASE_URL}/api/generate-alt-text",
            headers=HEADERS,
            json={
                "image_source": sample_images["essential_oils"],
                "source_type": "url",
                "product_name": "Organic Essential Oil Collection"
            }
        )
    )
    
    # 3. Batch Image Analysis
    print_response(
        "3. Batch Image Analysis",
        requests.post(
            f"{BASE_URL}/api/batch-analyze-images",
            headers=HEADERS,
            json={
                "images": [
                    {
                        "source": sample_images["turmeric"],
                        "type": "url",
                        "name": "turmeric_product"
                    },
                    {
                        "source": sample_images["essential_oils"],
                        "type": "url",
                        "name": "essential_oils_set"
                    }
                ]
            }
        )
    )

def test_recommendation_system():
    """Test recommendation system features"""
    print("\n🎯 TESTING RECOMMENDATION SYSTEM")
    print("=" * 50)
    
    # 1. Train Recommendation Model
    print("Training recommendation model (this may take a minute)...")
    print_response(
        "1. Train Recommendation Model",
        requests.post(
            f"{BASE_URL}/api/train-recommendations",
            headers=HEADERS,
            json={
                "use_sample_data": True,
                "algorithm": "SVD"
            }
        )
    )
    
    # Wait a moment for model to be saved
    time.sleep(2)
    
    # 2. Get User Recommendations
    print_response(
        "2. Get User Recommendations",
        requests.get(f"{BASE_URL}/api/user-recommendations/user_10?n_recommendations=5")
    )
    
    # 3. Get Item Recommendations
    print_response(
        "3. Get Similar Items",
        requests.get(f"{BASE_URL}/api/item-recommendations/Turmeric CO2 Extract?n_recommendations=5")
    )
    
    # 4. Get Popular Items
    print_response(
        "4. Get Popular Items",
        requests.get(f"{BASE_URL}/api/popular-items?n_items=10&min_ratings=5")
    )
    
    # 5. Predict Rating
    print_response(
        "5. Predict User Rating",
        requests.post(
            f"{BASE_URL}/api/predict-rating",
            headers=HEADERS,
            json={
                "user_id": "user_25",
                "item_id": "Lavender Oil"
            }
        )
    )
    
    # 6. Get Model Statistics
    print_response(
        "6. Get Model Statistics",
        requests.get(f"{BASE_URL}/api/model-stats")
    )

def test_complete_automation():
    """Test complete product automation pipeline"""
    print("\n🔄 TESTING COMPLETE AUTOMATION PIPELINE")
    print("=" * 50)
    
    print("Running complete product automation (this may take a minute)...")
    print_response(
        "Complete Product Automation",
        requests.post(
            f"{BASE_URL}/api/complete-product-automation",
            headers=HEADERS,
            json={
                "product_name": "Premium Lavender Essential Oil",
                "features": ["100% Pure", "Steam Distilled", "Calming", "Sleep Aid"],
                "category": "Essential Oils",
                "price": 24.99,
                "image_source": "https://images.unsplash.com/photo-1611909482911-0d829a5bfa9e?w=500",
                "source_type": "url"
            }
        )
    )

def run_performance_test():
    """Run basic performance tests"""
    print("\n⚡ RUNNING PERFORMANCE TESTS")
    print("=" * 50)
    
    # Test response times for different endpoints
    endpoints = [
        ("Health Check", "GET", "/health", {}),
        ("Product Description", "POST", "/api/generate-description", {
            "product_name": "Test Product",
            "features": ["Feature 1", "Feature 2"]
        }),
    ]
    
    for name, method, endpoint, data in endpoints:
        print(f"\nTesting {name}...")
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            print(f"✅ {name}: {response.status_code} - {response_time:.2f}ms")
            
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")

def demonstrate_error_handling():
    """Demonstrate API error handling"""
    print("\n🚨 TESTING ERROR HANDLING")
    print("=" * 50)
    
    # Test various error conditions
    error_tests = [
        ("Missing Required Field", "POST", "/api/generate-description", {"features": ["test"]}),
        ("Invalid Endpoint", "GET", "/api/nonexistent", {}),
        ("Invalid JSON", "POST", "/api/generate-seo", "invalid json"),
        ("Invalid Image URL", "POST", "/api/analyze-image", {
            "image_source": "not-a-url",
            "source_type": "url"
        })
    ]
    
    for name, method, endpoint, data in error_tests:
        print(f"\n{name}:")
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                if isinstance(data, str):
                    response = requests.post(f"{BASE_URL}{endpoint}", data=data)
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
            
            print(f"Status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"Exception: {str(e)}")

def main():
    """Main function to run API examples"""
    parser = argparse.ArgumentParser(description='API Testing and Examples')
    parser.add_argument('--test', choices=[
        'gemini', 'blip', 'recommendations', 'automation', 'performance', 'errors', 'all'
    ], default='all', help='Test suite to run')
    
    args = parser.parse_args()
    
    print("🚀 AI Automation System - API Examples")
    print("=" * 50)
    
    # Check if server is running
    if not check_server_health():
        sys.exit(1)
    
    try:
        if args.test == 'all':
            test_gemini_features()
            test_image_analysis()
            test_recommendation_system()
            test_complete_automation()
            run_performance_test()
            demonstrate_error_handling()
        elif args.test == 'gemini':
            test_gemini_features()
        elif args.test == 'blip':
            test_image_analysis()
        elif args.test == 'recommendations':
            test_recommendation_system()
        elif args.test == 'automation':
            test_complete_automation()
        elif args.test == 'performance':
            run_performance_test()
        elif args.test == 'errors':
            demonstrate_error_handling()
        
        print("\n✅ API testing completed successfully!")
        print("\n📝 Tips:")
        print("   • All endpoints return JSON with 'success' and 'data' fields")
        print("   • Error responses include 'error' field with details")
        print("   • Use /health endpoint to check server status")
        print("   • Check server logs for detailed error information")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    main()
