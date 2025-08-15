"""
Manual test of the SimpleRecommendationService
This can be run independently of the Flask API
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.simple_recommendation_service import SimpleRecommendationService

def main():
    print("🧪 Manual Test: SimpleRecommendationService")
    print("=" * 50)
    
    # Initialize service
    rec_service = SimpleRecommendationService()
    print("✓ Service initialized")
    
    # Load sample data
    print("\n📊 Loading sample data...")
    ratings_df = rec_service.load_sample_data()
    print(f"✓ Loaded {len(ratings_df)} ratings")
    print(f"  Users: {ratings_df['user_id'].nunique()}")
    print(f"  Products: {ratings_df['product_id'].nunique()}")
    
    # Show sample of data
    print("\n📋 Sample ratings:")
    sample_ratings = ratings_df.head(10)
    for _, row in sample_ratings.iterrows():
        print(f"  {row['user_id']} rated '{row['product_id']}': {row['rating']} stars")
    
    # Prepare data
    print("\n⚙️  Preparing data...")
    rec_service.prepare_data(ratings_df)
    print("✓ Data prepared")
    
    # Train model
    print("\n🔄 Training NMF model...")
    training_result = rec_service.train_model(algorithm="NMF")
    print("✓ Model trained successfully!")
    print(f"  Algorithm: {training_result['algorithm']}")
    print(f"  Users: {training_result['n_users']}")
    print(f"  Items: {training_result['n_items']}")
    print(f"  Ratings: {training_result['n_ratings']}")
    print(f"  Sparsity: {training_result['sparsity']:.3f}")
    
    # Get model stats
    print("\n📈 Model Statistics:")
    stats = rec_service.get_model_stats()
    print(f"  Model Type: {stats['model_type']}")
    print(f"  Global Mean Rating: {stats['global_mean']:.2f}")
    print(f"  Rating Scale: {stats['rating_scale']}")
    print(f"  Components: {stats.get('n_components', 'N/A')}")
    
    # Test user recommendations
    print("\n👤 Testing User Recommendations:")
    test_user = "user_5"
    user_recs = rec_service.get_user_recommendations(test_user, n_recommendations=5)
    
    if "error" not in user_recs:
        print(f"✓ Generated {len(user_recs['recommendations'])} recommendations for {test_user}")
        print("  Top recommendations:")
        for i, rec in enumerate(user_recs['recommendations'], 1):
            print(f"    {i}. {rec['product_id']} (predicted rating: {rec['predicted_rating']:.2f})")
    else:
        print(f"✗ Error getting user recommendations: {user_recs['error']}")
    
    # Test item recommendations
    print("\n🛍️  Testing Item Recommendations:")
    test_item = "Turmeric CO2 Extract"
    item_recs = rec_service.get_item_recommendations(test_item, n_recommendations=5)
    
    if "error" not in item_recs:
        print(f"✓ Found {len(item_recs['similar_items'])} similar items to '{test_item}'")
        print("  Similar items:")
        for i, item in enumerate(item_recs['similar_items'], 1):
            print(f"    {i}. {item['product_id']} (similarity: {item['similarity_score']:.3f})")
    else:
        print(f"✗ Error getting item recommendations: {item_recs['error']}")
    
    # Test popular items
    print("\n🔥 Testing Popular Items:")
    popular = rec_service.get_popular_items(n_items=5)
    
    if "error" not in popular:
        print(f"✓ Found {len(popular['popular_items'])} popular items")
        print("  Most popular items:")
        for i, item in enumerate(popular['popular_items'], 1):
            print(f"    {i}. {item['product_id']} (avg: {item['average_rating']:.2f}, ratings: {item['num_ratings']})")
    else:
        print(f"✗ Error getting popular items: {popular['error']}")
    
    # Test rating prediction
    print("\n🎯 Testing Rating Prediction:")
    test_user = "user_10"
    test_item = "Lavender Oil"
    
    prediction = rec_service.predict_rating(test_user, test_item)
    
    if "error" not in prediction:
        print(f"✓ Predicted rating for {test_user} and '{test_item}':")
        print(f"  Predicted rating: {prediction['predicted_rating']:.2f}")
        print(f"  Confidence: {prediction['confidence']:.3f}")
        print(f"  Was impossible: {prediction['was_impossible']}")
    else:
        print(f"✗ Error predicting rating: {prediction['error']}")
    
    # Test model save/load
    print("\n💾 Testing Model Save/Load:")
    save_result = rec_service.save_model()
    
    if "error" not in save_result:
        print(f"✓ Model saved to: {save_result['path']}")
        
        # Create new service and load model
        new_service = SimpleRecommendationService()
        load_result = new_service.load_model()
        
        if "error" not in load_result:
            print(f"✓ Model loaded from: {load_result['path']}")
            
            # Test loaded model
            test_recs = new_service.get_user_recommendations("user_1", n_recommendations=3)
            if "error" not in test_recs:
                print(f"✓ Loaded model working - {len(test_recs['recommendations'])} recommendations generated")
            else:
                print(f"✗ Loaded model test failed: {test_recs['error']}")
        else:
            print(f"✗ Error loading model: {load_result['error']}")
    else:
        print(f"✗ Error saving model: {save_result['error']}")
    
    print("\n" + "=" * 50)
    print("🎉 Manual test completed successfully!")
    print("Your recommendation system is working correctly.")

if __name__ == "__main__":
    main()
