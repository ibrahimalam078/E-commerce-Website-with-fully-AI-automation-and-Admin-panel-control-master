#!/usr/bin/env python3
"""
Test script for recommendation system features
Run individual recommendation automation features using Surprise library
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.simple_recommendation_service import SimpleRecommendationService as RecommendationService
import json
import argparse
import pandas as pd

def test_sample_data_generation():
    """Test sample data generation"""
    print("📊 Testing Sample Data Generation...")
    
    service = RecommendationService()
    
    try:
        # Generate sample data
        ratings_df = service.load_sample_data()
        
        print(f"✅ Sample data generated:")
        print(f"📊 Total ratings: {len(ratings_df)}")
        print(f"👥 Unique users: {ratings_df['user_id'].nunique()}")
        print(f"📦 Unique products: {ratings_df['product_id'].nunique()}")
        print(f"⭐ Rating range: {ratings_df['rating'].min()} - {ratings_df['rating'].max()}")
        
        # Show sample data
        print(f"\n📝 Sample ratings:")
        print(ratings_df.head(10).to_string(index=False))
        
        # Show product distribution
        print(f"\n📦 Top 10 most rated products:")
        product_counts = ratings_df['product_id'].value_counts().head(10)
        for product, count in product_counts.items():
            print(f"   • {product}: {count} ratings")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_model_training():
    """Test model training with different algorithms"""
    print("\n🤖 Testing Model Training...")
    
    service = RecommendationService()
    
    algorithms = ["NMF"]
    
    for algorithm in algorithms:
        print(f"\n🔧 Training with {algorithm}...")
        
        try:
            # Generate and prepare sample data
            ratings_df = service.load_sample_data()
            service.prepare_data(ratings_df)
            
            # Train model
            result = service.train_model(algorithm=algorithm)
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ {algorithm} model trained successfully:")
                print(f"📊 RMSE: {result.get('rmse', 'N/A'):.3f}")
                print(f"📊 MAE: {result.get('mae', 'N/A'):.3f}")
                print(f"🔄 CV RMSE: {result.get('cv_rmse_mean', 'N/A'):.3f}")
                print(f"👥 Users: {result.get('n_users', 'N/A')}")
                print(f"📦 Items: {result.get('n_items', 'N/A')}")
                print(f"⭐ Ratings: {result.get('n_ratings', 'N/A')}")
                
                # Save the model
                save_result = service.save_model()
                if "error" not in save_result:
                    print(f"💾 Model saved: {save_result.get('path', 'Unknown')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_user_recommendations():
    """Test personalized user recommendations"""
    print("\n👤 Testing User Recommendations...")
    
    service = RecommendationService()
    
    # Try to load existing model or train a new one
    if not os.path.exists("simple_recommendation_model.pkl"):
        print("📦 No existing model found. Training new model...")
        ratings_df = service.load_sample_data()
        service.prepare_data(ratings_df)
        service.train_model("NMF")
        service.save_model()
    else:
        print("📦 Loading existing model...")
        service.load_model()
    
    # Test users (from our sample data)
    test_users = ["user_1", "user_25", "user_50", "user_75"]
    
    for user_id in test_users:
        print(f"\n👤 Recommendations for {user_id}:")
        
        try:
            result = service.get_user_recommendations(
                user_id=user_id,
                n_recommendations=5,
                exclude_rated=True
            )
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                recommendations = result.get('recommendations', [])
                excluded_count = result.get('excluded_rated_items', 0)
                
                print(f"🎯 Found {len(recommendations)} recommendations (excluded {excluded_count} rated items):")
                
                for i, rec in enumerate(recommendations, 1):
                    product_id = rec.get('product_id', 'Unknown')
                    predicted_rating = rec.get('predicted_rating', 0)
                    confidence = rec.get('confidence', 0)
                    
                    print(f"   {i}. {product_id}")
                    print(f"      ⭐ Predicted rating: {predicted_rating:.2f}")
                    print(f"      🎯 Confidence: {confidence:.2f}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_item_recommendations():
    """Test item-to-item recommendations"""
    print("\n📦 Testing Item Recommendations...")
    
    service = RecommendationService()
    
    # Load model
    if service.model is None:
        if os.path.exists("simple_recommendation_model.pkl"):
            service.load_model()
        else:
            print("❌ No model available. Please train a model first.")
            return
    
    # Test products (from our sample data)
    test_products = [
        "Turmeric CO2 Extract",
        "Lavender Oil", 
        "Tea Tree Oil",
        "Coconut Oil"
    ]
    
    for product_id in test_products:
        print(f"\n📦 Similar items to '{product_id}':")
        
        try:
            result = service.get_item_recommendations(
                item_id=product_id,
                n_recommendations=5
            )
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                similar_items = result.get('similar_items', [])
                
                if similar_items:
                    print(f"🔍 Found {len(similar_items)} similar items:")
                    
                    for i, item in enumerate(similar_items, 1):
                        similar_product = item.get('product_id', 'Unknown')
                        similarity = item.get('similarity_score', 0)
                        confidence = item.get('confidence', 0)
                        
                        print(f"   {i}. {similar_product}")
                        print(f"      🔗 Similarity: {similarity:.3f}")
                        print(f"      🎯 Confidence: {confidence:.3f}")
                else:
                    print("   📝 No similar items found (item may not be in training data)")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_popular_items():
    """Test popular items recommendation"""
    print("\n🔥 Testing Popular Items...")
    
    service = RecommendationService()
    
    # Load model
    if service.model is None:
        if os.path.exists("simple_recommendation_model.pkl"):
            service.load_model()
        else:
            print("❌ No model available. Please train a model first.")
            return
    
    try:
        result = service.get_popular_items(
            n_items=10,
            min_ratings=5
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            popular_items = result.get('popular_items', [])
            min_threshold = result.get('min_ratings_threshold', 0)
            total_qualifying = result.get('total_qualifying_items', 0)
            
            print(f"🔥 Top {len(popular_items)} popular items (min {min_threshold} ratings):")
            print(f"📊 Total qualifying items: {total_qualifying}")
            
            for i, item in enumerate(popular_items, 1):
                product_id = item.get('product_id', 'Unknown')
                avg_rating = item.get('average_rating', 0)
                num_ratings = item.get('num_ratings', 0)
                weighted_score = item.get('weighted_score', 0)
                
                print(f"\n   {i}. {product_id}")
                print(f"      ⭐ Average rating: {avg_rating:.2f}")
                print(f"      📊 Number of ratings: {num_ratings}")
                print(f"      🏆 Weighted score: {weighted_score:.2f}")
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_rating_prediction():
    """Test rating prediction for specific user-item pairs"""
    print("\n🎯 Testing Rating Prediction...")
    
    service = RecommendationService()
    
    # Load model
    if service.model is None:
        if os.path.exists("simple_recommendation_model.pkl"):
            service.load_model()
        else:
            print("❌ No model available. Please train a model first.")
            return
    
    # Test cases: user-item pairs
    test_cases = [
        ("user_10", "Turmeric CO2 Extract"),
        ("user_20", "Lavender Oil"),
        ("user_30", "Tea Tree Oil"),
        ("user_40", "Coconut Oil"),
        ("new_user_123", "Peppermint Oil")  # New user not in training data
    ]
    
    for user_id, item_id in test_cases:
        print(f"\n🎯 Predicting rating for {user_id} → {item_id}:")
        
        try:
            result = service.predict_rating(
                user_id=user_id,
                item_id=item_id
            )
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                predicted_rating = result.get('predicted_rating', 0)
                was_impossible = result.get('was_impossible', False)
                confidence = result.get('confidence', 0)
                
                print(f"   ⭐ Predicted rating: {predicted_rating:.2f}")
                print(f"   🎯 Confidence: {confidence:.2f}")
                
                if was_impossible:
                    print(f"   ⚠️ Prediction was impossible (cold start problem)")
                else:
                    print(f"   ✅ Prediction successful")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_model_statistics():
    """Test model statistics and information"""
    print("\n📊 Testing Model Statistics...")
    
    service = RecommendationService()
    
    # Load model
    if service.model is None:
        if os.path.exists("simple_recommendation_model.pkl"):
            service.load_model()
        else:
            print("❌ No model available. Please train a model first.")
            return
    
    try:
        result = service.get_model_stats()
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("📊 Model Statistics:")
            print(f"   🤖 Model Type: {result.get('model_type', 'Unknown')}")
            print(f"   👥 Number of Users: {result.get('n_users', 'Unknown')}")
            print(f"   📦 Number of Items: {result.get('n_items', 'Unknown')}")
            print(f"   ⭐ Number of Ratings: {result.get('n_ratings', 'Unknown')}")
            print(f"   📏 Rating Scale: {result.get('rating_scale', 'Unknown')}")
            print(f"   📊 Global Mean Rating: {result.get('global_mean', 0):.2f}")
            print(f"   🕳️ Data Sparsity: {result.get('sparsity', 0):.2%}")
            
            # Algorithm-specific stats
            if 'n_factors' in result:
                print(f"   🧮 Number of Factors: {result['n_factors']}")
            if 'n_epochs' in result:
                print(f"   🔄 Number of Epochs: {result['n_epochs']}")
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def main():
    """Main function to run tests"""
    parser = argparse.ArgumentParser(description='Test Recommendation System Features')
    parser.add_argument('--feature', choices=[
        'data', 'train', 'user-recs', 'item-recs', 'popular', 'predict', 'stats', 'all'
    ], default='all', help='Feature to test')
    
    args = parser.parse_args()
    
    print("🎯 Recommendation System Testing")
    print("=" * 50)
    print("📝 Note: Training may take some time on first run")
    print()
    
    try:
        if args.feature == 'all':
            test_sample_data_generation()
            test_model_training()
            test_user_recommendations()
            test_item_recommendations()
            test_popular_items()
            test_rating_prediction()
            test_model_statistics()
        elif args.feature == 'data':
            test_sample_data_generation()
        elif args.feature == 'train':
            test_model_training()
        elif args.feature == 'user-recs':
            test_user_recommendations()
        elif args.feature == 'item-recs':
            test_item_recommendations()
        elif args.feature == 'popular':
            test_popular_items()
        elif args.feature == 'predict':
            test_rating_prediction()
        elif args.feature == 'stats':
            test_model_statistics()
        
        print("\n✅ Testing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
