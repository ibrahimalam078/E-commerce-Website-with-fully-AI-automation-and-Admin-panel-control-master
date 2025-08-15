"""
Enhanced Test Runner for AI Automation System
Manages Flask server and runs comprehensive API tests
"""
import sys
import time
import requests
import json
from start_server import FlaskServerManager

class APITestRunner:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.test_results = {}
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        self.test_results[test_name] = {
            'success': success,
            'details': details
        }
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                details = f"Status: {data['status']}, Services: {list(data['services'].keys())}"
                self.log_test("Health Check", True, details)
                return True
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, str(e))
            return False
    
    def test_recommendation_training(self):
        """Test recommendation model training"""
        try:
            payload = {
                "use_sample_data": True,
                "algorithm": "NMF"
            }
            
            response = requests.post(
                f"{self.base_url}/api/train-recommendations",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()['data']
                details = f"Algorithm: {data['algorithm']}, Users: {data['n_users']}, Items: {data['n_items']}, Ratings: {data['n_ratings']}"
                self.log_test("Recommendation Training", True, details)
                return True
            else:
                self.log_test("Recommendation Training", False, f"HTTP {response.status_code}: {response.text[:100]}")
                return False
        except Exception as e:
            self.log_test("Recommendation Training", False, str(e))
            return False
    
    def test_user_recommendations(self):
        """Test getting user recommendations"""
        try:
            user_id = "user_5"
            response = requests.get(f"{self.base_url}/api/user-recommendations/{user_id}?n_recommendations=5", timeout=10)
            
            if response.status_code == 200:
                data = response.json()['data']
                recs = data['recommendations']
                details = f"Found {len(recs)} recommendations for {user_id}"
                if recs:
                    details += f", Top: {recs[0]['product_id']} ({recs[0]['predicted_rating']:.2f})"
                self.log_test("User Recommendations", True, details)
                return True
            else:
                self.log_test("User Recommendations", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("User Recommendations", False, str(e))
            return False
    
    def test_item_recommendations(self):
        """Test getting similar item recommendations"""
        try:
            item_id = "Turmeric CO2 Extract"
            response = requests.get(f"{self.base_url}/api/item-recommendations/{item_id}?n_recommendations=5", timeout=10)
            
            if response.status_code == 200:
                data = response.json()['data']
                similar = data['similar_items']
                details = f"Found {len(similar)} similar items to '{item_id}'"
                if similar:
                    details += f", Top: {similar[0]['product_id']} ({similar[0]['similarity_score']:.3f})"
                self.log_test("Item Recommendations", True, details)
                return True
            else:
                self.log_test("Item Recommendations", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Item Recommendations", False, str(e))
            return False
    
    def test_popular_items(self):
        """Test getting popular items"""
        try:
            response = requests.get(f"{self.base_url}/api/popular-items?n_items=5", timeout=10)
            
            if response.status_code == 200:
                data = response.json()['data']
                popular = data['popular_items']
                details = f"Found {len(popular)} popular items"
                if popular:
                    top_item = popular[0]
                    details += f", Top: {top_item['product_id']} (avg: {top_item['average_rating']:.2f})"
                self.log_test("Popular Items", True, details)
                return True
            else:
                self.log_test("Popular Items", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Popular Items", False, str(e))
            return False
    
    def test_rating_prediction(self):
        """Test rating prediction"""
        try:
            payload = {
                "user_id": "user_10",
                "item_id": "Lavender Oil"
            }
            
            response = requests.post(
                f"{self.base_url}/api/predict-rating",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()['data']
                details = f"Predicted {data['predicted_rating']:.2f} for {data['user_id']} + {data['item_id']}"
                self.log_test("Rating Prediction", True, details)
                return True
            else:
                self.log_test("Rating Prediction", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Rating Prediction", False, str(e))
            return False
    
    def test_gemini_description(self):
        """Test Gemini AI product description generation"""
        try:
            payload = {
                "product_name": "Organic Turmeric Essential Oil",
                "features": ["100% pure", "organic", "anti-inflammatory", "natural"],
                "category": "Essential Oils"
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate-description",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()['data']
                description = data.get('description', '')
                details = f"Generated {len(description)} character description"
                self.log_test("Gemini Description Generation", True, details)
                return True
            else:
                self.log_test("Gemini Description Generation", False, f"HTTP {response.status_code}: {response.text[:100]}")
                return False
        except Exception as e:
            self.log_test("Gemini Description Generation", False, str(e))
            return False
    
    def test_gemini_categories(self):
        """Test Gemini AI category generation"""
        try:
            payload = {
                "product_name": "Lavender Essential Oil",
                "description": "Pure lavender oil for aromatherapy and relaxation"
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate-categories",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()['data']
                categories = data.get('categories', [])
                tags = data.get('tags', [])
                details = f"Generated {len(categories)} categories, {len(tags)} tags"
                self.log_test("Gemini Category Generation", True, details)
                return True
            else:
                self.log_test("Gemini Category Generation", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Gemini Category Generation", False, str(e))
            return False
    
    def test_model_stats(self):
        """Test getting model statistics"""
        try:
            response = requests.get(f"{self.base_url}/api/model-stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()['data']
                details = f"Model: {data['model_type']}, Mean: {data['global_mean']:.2f}, Users: {data['n_users']}, Items: {data['n_items']}"
                self.log_test("Model Statistics", True, details)
                return True
            else:
                self.log_test("Model Statistics", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Model Statistics", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 AI Automation System - Comprehensive API Test Suite")
        print("=" * 60)
        
        tests = [
            self.test_health_endpoint,
            self.test_recommendation_training,
            self.test_user_recommendations,
            self.test_item_recommendations,
            self.test_popular_items,
            self.test_rating_prediction,
            self.test_model_stats,
            self.test_gemini_description,
            self.test_gemini_categories,
        ]
        
        results = []
        for i, test in enumerate(tests, 1):
            print(f"\n[{i}/{len(tests)}] Running {test.__name__.replace('test_', '').replace('_', ' ').title()}...")
            try:
                success = test()
                results.append(success)
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {str(e)}")
                results.append(False)
        
        print("\n" + "=" * 60)
        print("📊 Test Results Summary:")
        print(f"  ✅ Passed: {sum(results)}")
        print(f"  ❌ Failed: {len(results) - sum(results)}")
        print(f"  📈 Success Rate: {sum(results)/len(results)*100:.1f}%")
        
        if all(results):
            print("\n🎉 All tests passed! Your AI automation system is working perfectly.")
        else:
            print("\n⚠️  Some tests failed. Check the details above.")
            
        return results

def main():
    """Main test runner function"""
    print("🔧 Starting AI Automation System Test Suite")
    
    # Initialize server manager
    server = FlaskServerManager()
    
    try:
        # Start the Flask server
        if server.start(timeout=45):
            print("✅ Server started successfully!")
            
            # Wait a moment for full initialization
            time.sleep(3)
            
            # Run all tests
            test_runner = APITestRunner()
            results = test_runner.run_all_tests()
            
            # Additional integration examples
            print(f"\n🔗 Integration Examples:")
            print(f"   Base URL: {test_runner.base_url}")
            print(f"   Health Check: GET {test_runner.base_url}/health")
            print(f"   Train Model: POST {test_runner.base_url}/api/train-recommendations")
            print(f"   Get Recommendations: GET {test_runner.base_url}/api/user-recommendations/user_5")
            print(f"   Generate Description: POST {test_runner.base_url}/api/generate-description")
            
            return all(results)
            
        else:
            print("❌ Failed to start Flask server")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Test suite error: {str(e)}")
        return False
    finally:
        # Always stop the server
        server.stop()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
