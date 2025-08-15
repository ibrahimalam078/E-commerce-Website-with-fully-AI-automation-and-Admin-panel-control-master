"""
Test script to verify API endpoints work correctly
Run this after starting the Flask server with: python app.py
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_health_endpoint():
    """Test health check endpoint"""
    try:
        print("Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check successful: {data['status']}")
            print(f"  Services: {data['services']}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {str(e)}")
        return False

def test_recommendation_training():
    """Test recommendation model training"""
    try:
        print("\nTesting recommendation model training...")
        
        payload = {
            "use_sample_data": True,
            "algorithm": "NMF"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/train-recommendations",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Recommendation model training successful!")
            print(f"  Algorithm: {data['data']['algorithm']}")
            print(f"  Users: {data['data']['n_users']}")
            print(f"  Items: {data['data']['n_items']}")
            print(f"  Ratings: {data['data']['n_ratings']}")
            print(f"  Sparsity: {data['data']['sparsity']:.3f}")
            return True
        else:
            print(f"✗ Training failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Training error: {str(e)}")
        return False

def test_user_recommendations():
    """Test getting user recommendations"""
    try:
        print("\nTesting user recommendations...")
        
        user_id = "user_5"
        response = requests.get(f"{BASE_URL}/api/user-recommendations/{user_id}?n_recommendations=5")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ User recommendations successful for {user_id}!")
            recommendations = data['data']['recommendations']
            print(f"  Found {len(recommendations)} recommendations:")
            
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"    {i}. {rec['product_id']} (rating: {rec['predicted_rating']:.2f})")
            
            return True
        else:
            print(f"✗ User recommendations failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ User recommendations error: {str(e)}")
        return False

def test_item_recommendations():
    """Test getting item recommendations"""
    try:
        print("\nTesting item recommendations...")
        
        item_id = "Turmeric CO2 Extract"
        response = requests.get(f"{BASE_URL}/api/item-recommendations/{item_id}?n_recommendations=5")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Item recommendations successful for '{item_id}'!")
            similar_items = data['data']['similar_items']
            print(f"  Found {len(similar_items)} similar items:")
            
            for i, item in enumerate(similar_items[:3], 1):
                print(f"    {i}. {item['product_id']} (similarity: {item['similarity_score']:.3f})")
            
            return True
        else:
            print(f"✗ Item recommendations failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Item recommendations error: {str(e)}")
        return False

def test_popular_items():
    """Test getting popular items"""
    try:
        print("\nTesting popular items...")
        
        response = requests.get(f"{BASE_URL}/api/popular-items?n_items=5")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Popular items successful!")
            popular_items = data['data']['popular_items']
            print(f"  Found {len(popular_items)} popular items:")
            
            for i, item in enumerate(popular_items[:3], 1):
                print(f"    {i}. {item['product_id']} (avg: {item['average_rating']:.2f}, count: {item['num_ratings']})")
            
            return True
        else:
            print(f"✗ Popular items failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Popular items error: {str(e)}")
        return False

def test_rating_prediction():
    """Test rating prediction"""
    try:
        print("\nTesting rating prediction...")
        
        payload = {
            "user_id": "user_10",
            "item_id": "Lavender Oil"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/predict-rating",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Rating prediction successful!")
            prediction = data['data']
            print(f"  User: {prediction['user_id']}")
            print(f"  Item: {prediction['item_id']}")
            print(f"  Predicted rating: {prediction['predicted_rating']:.2f}")
            print(f"  Confidence: {prediction['confidence']:.3f}")
            return True
        else:
            print(f"✗ Rating prediction failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Rating prediction error: {str(e)}")
        return False

def test_gemini_description():
    """Test Gemini AI product description generation"""
    try:
        print("\nTesting Gemini AI product description...")
        
        payload = {
            "product_name": "Organic Turmeric Essential Oil",
            "features": ["100% pure", "organic", "anti-inflammatory", "natural"],
            "category": "Essential Oils"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/generate-description",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Product description generation successful!")
            description = data['data']['description']
            print(f"  Description preview: {description[:100]}...")
            return True
        else:
            print(f"✗ Description generation failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Description generation error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Automation System API Test Suite")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    tests = [
        test_health_endpoint,
        test_recommendation_training,
        test_user_recommendations, 
        test_item_recommendations,
        test_popular_items,
        test_rating_prediction,
        test_gemini_description,
    ]
    
    results = []
    for test in tests:
        success = test()
        results.append(success)
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"  ✓ Passed: {sum(results)}")
    print(f"  ✗ Failed: {len(results) - sum(results)}")
    print(f"  📈 Success Rate: {sum(results)/len(results)*100:.1f}%")
    
    if all(results):
        print("\n🎉 All tests passed! Your AI automation system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
