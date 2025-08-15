"""
Product Recommendation Service
Handles personalized recommendations using the Surprise library for collaborative filtering
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF
from sklearn.model_selection import train_test_split
import logging
from typing import Dict, List, Any, Optional, Tuple
from config import Config
import pickle
import os
from collections import defaultdict

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service class for product recommendation operations"""
    
    def __init__(self):
        """Initialize recommendation service"""
        self.model = None
        self.trainset = None
        self.testset = None
        self.user_item_matrix = None
        self.item_features = {}
        self.user_features = {}
        self.model_path = "recommendation_model.pkl"
        
    def load_sample_data(self) -> pd.DataFrame:
        """
        Load sample e-commerce data for testing
        
        Returns:
            DataFrame with user ratings data
        """
        # Generate sample data for natural products e-commerce
        np.random.seed(42)
        
        users = [f"user_{i}" for i in range(1, 101)]  # 100 users
        products = [
            "Turmeric CO2 Extract", "Clove Essential Oil", "Black Pepper Oleoresin",
            "Lavender Oil", "Tea Tree Oil", "Eucalyptus Oil", "Peppermint Oil",
            "Rosemary Extract", "Ginger Extract", "Garlic Extract", "Aloe Vera Gel",
            "Coconut Oil", "Argan Oil", "Jojoba Oil", "Sweet Almond Oil",
            "Frankincense Oil", "Lemon Oil", "Orange Oil", "Bergamot Oil",
            "Ylang Ylang Oil", "Sandalwood Oil", "Cedarwood Oil", "Pine Oil",
            "Chamomile Extract", "Green Tea Extract", "Vitamin E Oil",
            "Moringa Powder", "Spirulina Powder", "Wheatgrass Powder",
            "Ashwagandha Extract"
        ]
        
        # Generate ratings data
        ratings_data = []
        for user in users:
            # Each user rates 10-20 random products
            num_ratings = np.random.randint(10, 21)
            user_products = np.random.choice(products, num_ratings, replace=False)
            
            for product in user_products:
                # Generate ratings with some bias based on product popularity
                if product in ["Turmeric CO2 Extract", "Lavender Oil", "Tea Tree Oil"]:
                    rating = np.random.choice([4, 5], p=[0.3, 0.7])
                elif product in ["Coconut Oil", "Aloe Vera Gel", "Peppermint Oil"]:
                    rating = np.random.choice([3, 4, 5], p=[0.2, 0.4, 0.4])
                else:
                    rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.3, 0.35, 0.2])
                
                ratings_data.append({
                    'user_id': user,
                    'product_id': product,
                    'rating': rating
                })
        
        return pd.DataFrame(ratings_data)
    
    def prepare_data(self, ratings_df: pd.DataFrame) -> None:
        """
        Prepare data for training
        
        Args:
            ratings_df: DataFrame with columns ['user_id', 'product_id', 'rating']
        """
        try:
            # Define the rating scale
            reader = Reader(rating_scale=(1, 5))
            
            # Load data into Surprise dataset
            data = Dataset.load_from_df(ratings_df[['user_id', 'product_id', 'rating']], reader)
            
            # Split into train and test sets
            self.trainset, self.testset = train_test_split(data, test_size=0.2, random_state=42)
            
            # Create user-item matrix for analysis
            self.user_item_matrix = ratings_df.pivot(index='user_id', columns='product_id', values='rating').fillna(0)
            
            logger.info(f"Data prepared: {len(ratings_df)} ratings, {ratings_df['user_id'].nunique()} users, {ratings_df['product_id'].nunique()} items")
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
    
    def train_model(self, algorithm: str = "SVD") -> Dict[str, Any]:
        """
        Train recommendation model
        
        Args:
            algorithm: Algorithm to use ("SVD", "KNNBasic")
            
        Returns:
            Dict containing training results
        """
        try:
            if self.trainset is None:
                raise ValueError("Data not prepared. Call prepare_data() first.")
            
            # Choose algorithm
            if algorithm == "SVD":
                self.model = SVD(n_factors=50, n_epochs=20, lr_all=0.005, reg_all=0.02, random_state=42)
            elif algorithm == "KNNBasic":
                self.model = KNNBasic(k=40, sim_options={'name': 'cosine', 'user_based': False})
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
            
            # Train model
            self.model.fit(self.trainset)
            
            # Evaluate model
            predictions = self.model.test(self.testset)
            rmse = accuracy.rmse(predictions, verbose=False)
            mae = accuracy.mae(predictions, verbose=False)
            
            # Cross-validation
            cv_results = cross_validate(self.model, Dataset.load_from_df(
                pd.DataFrame([(uid, iid, rating) for uid, iid, rating in self.trainset.all_ratings()], 
                            columns=['user_id', 'product_id', 'rating']),
                Reader(rating_scale=(1, 5))
            ), measures=['RMSE', 'MAE'], cv=5, verbose=False)
            
            results = {
                "algorithm": algorithm,
                "rmse": rmse,
                "mae": mae,
                "cv_rmse_mean": np.mean(cv_results['test_rmse']),
                "cv_mae_mean": np.mean(cv_results['test_mae']),
                "n_users": self.trainset.n_users,
                "n_items": self.trainset.n_items,
                "n_ratings": len(self.trainset.all_ratings()),
                "trained_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Model trained successfully. RMSE: {rmse:.3f}, MAE: {mae:.3f}")
            return results
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {"error": str(e)}
    
    def save_model(self, model_path: str = None) -> Dict[str, Any]:
        """
        Save trained model to disk
        
        Args:
            model_path: Path to save the model
            
        Returns:
            Dict containing save status
        """
        try:
            if self.model is None:
                raise ValueError("No model to save. Train a model first.")
            
            save_path = model_path or self.model_path
            
            model_data = {
                'model': self.model,
                'trainset': self.trainset,
                'user_item_matrix': self.user_item_matrix,
                'item_features': self.item_features,
                'user_features': self.user_features
            }
            
            with open(save_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Model saved to {save_path}")
            return {"status": "success", "path": save_path}
            
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return {"error": str(e)}
    
    def load_model(self, model_path: str = None) -> Dict[str, Any]:
        """
        Load trained model from disk
        
        Args:
            model_path: Path to load the model from
            
        Returns:
            Dict containing load status
        """
        try:
            load_path = model_path or self.model_path
            
            if not os.path.exists(load_path):
                raise FileNotFoundError(f"Model file not found: {load_path}")
            
            with open(load_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.trainset = model_data['trainset']
            self.user_item_matrix = model_data.get('user_item_matrix')
            self.item_features = model_data.get('item_features', {})
            self.user_features = model_data.get('user_features', {})
            
            logger.info(f"Model loaded from {load_path}")
            return {"status": "success", "path": load_path}
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return {"error": str(e)}
    
    def get_user_recommendations(self, user_id: str, n_recommendations: int = 10,
                               exclude_rated: bool = True) -> Dict[str, Any]:
        """
        Get personalized recommendations for a user
        
        Args:
            user_id: User ID to get recommendations for
            n_recommendations: Number of recommendations to return
            exclude_rated: Whether to exclude already rated items
            
        Returns:
            Dict containing recommendations
        """
        try:
            if self.model is None:
                raise ValueError("Model not trained. Train or load a model first.")
            
            # Get all items
            all_items = self.trainset.all_items()
            
            # Get user's rated items if excluding them
            rated_items = set()
            if exclude_rated and self.user_item_matrix is not None:
                try:
                    user_ratings = self.user_item_matrix.loc[user_id]
                    rated_items = set(user_ratings[user_ratings > 0].index)
                except KeyError:
                    # User not in training data
                    pass
            
            # Generate predictions for all items
            predictions = []
            for item_raw_id in all_items:
                item_id = self.trainset.to_raw_iid(item_raw_id)
                
                if exclude_rated and item_id in rated_items:
                    continue
                
                prediction = self.model.predict(user_id, item_id)
                predictions.append({
                    'product_id': item_id,
                    'predicted_rating': prediction.est,
                    'confidence': 1 - abs(prediction.est - round(prediction.est))
                })
            
            # Sort by predicted rating and take top N
            predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
            top_recommendations = predictions[:n_recommendations]
            
            result = {
                "user_id": user_id,
                "recommendations": top_recommendations,
                "total_available": len(predictions),
                "excluded_rated_items": len(rated_items) if exclude_rated else 0,
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Generated {len(top_recommendations)} recommendations for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting user recommendations: {str(e)}")
            return {"error": str(e)}
    
    def get_item_recommendations(self, item_id: str, n_recommendations: int = 10) -> Dict[str, Any]:
        """
        Get similar item recommendations (item-to-item collaborative filtering)
        
        Args:
            item_id: Item ID to find similar items for
            n_recommendations: Number of similar items to return
            
        Returns:
            Dict containing similar items
        """
        try:
            if self.model is None:
                raise ValueError("Model not trained. Train or load a model first.")
            
            # For SVD, we'll use the item factors to find similar items
            if hasattr(self.model, 'qi'):
                try:
                    item_inner_id = self.trainset.to_inner_iid(item_id)
                    item_factors = self.model.qi[item_inner_id]
                    
                    # Calculate cosine similarity with all other items
                    similarities = []
                    for other_inner_id in range(self.trainset.n_items):
                        if other_inner_id == item_inner_id:
                            continue
                        
                        other_item_id = self.trainset.to_raw_iid(other_inner_id)
                        other_factors = self.model.qi[other_inner_id]
                        
                        # Cosine similarity
                        similarity = np.dot(item_factors, other_factors) / \
                                   (np.linalg.norm(item_factors) * np.linalg.norm(other_factors))
                        
                        similarities.append({
                            'product_id': other_item_id,
                            'similarity_score': float(similarity),
                            'confidence': float(abs(similarity))
                        })
                    
                    # Sort by similarity and take top N
                    similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
                    top_similar = similarities[:n_recommendations]
                    
                except ValueError:
                    # Item not in training data, return empty recommendations
                    top_similar = []
            else:
                # For other algorithms, use a different approach
                top_similar = []
            
            result = {
                "item_id": item_id,
                "similar_items": top_similar,
                "total_available": len(similarities) if 'similarities' in locals() else 0,
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Generated {len(top_similar)} similar items for {item_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting item recommendations: {str(e)}")
            return {"error": str(e)}
    
    def get_popular_items(self, n_items: int = 10, min_ratings: int = 5) -> Dict[str, Any]:
        """
        Get most popular items based on ratings
        
        Args:
            n_items: Number of popular items to return
            min_ratings: Minimum number of ratings required
            
        Returns:
            Dict containing popular items
        """
        try:
            if self.user_item_matrix is None:
                raise ValueError("User-item matrix not available")
            
            # Calculate popularity metrics
            item_stats = []
            for item in self.user_item_matrix.columns:
                ratings = self.user_item_matrix[item]
                ratings = ratings[ratings > 0]  # Only non-zero ratings
                
                if len(ratings) >= min_ratings:
                    avg_rating = ratings.mean()
                    num_ratings = len(ratings)
                    # Weighted score considering both rating and popularity
                    weighted_score = avg_rating * np.log(num_ratings + 1)
                    
                    item_stats.append({
                        'product_id': item,
                        'average_rating': float(avg_rating),
                        'num_ratings': int(num_ratings),
                        'weighted_score': float(weighted_score)
                    })
            
            # Sort by weighted score
            item_stats.sort(key=lambda x: x['weighted_score'], reverse=True)
            popular_items = item_stats[:n_items]
            
            result = {
                "popular_items": popular_items,
                "min_ratings_threshold": min_ratings,
                "total_qualifying_items": len(item_stats),
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Generated {len(popular_items)} popular items")
            return result
            
        except Exception as e:
            logger.error(f"Error getting popular items: {str(e)}")
            return {"error": str(e)}
    
    def predict_rating(self, user_id: str, item_id: str) -> Dict[str, Any]:
        """
        Predict rating for a specific user-item pair
        
        Args:
            user_id: User ID
            item_id: Item ID
            
        Returns:
            Dict containing predicted rating
        """
        try:
            if self.model is None:
                raise ValueError("Model not trained. Train or load a model first.")
            
            prediction = self.model.predict(user_id, item_id)
            
            result = {
                "user_id": user_id,
                "item_id": item_id,
                "predicted_rating": float(prediction.est),
                "was_impossible": prediction.details.get('was_impossible', False),
                "confidence": 1 - abs(prediction.est - round(prediction.est)),
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Predicted rating: {prediction.est:.2f} for user {user_id}, item {item_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error predicting rating: {str(e)}")
            return {"error": str(e)}
    
    def get_model_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the trained model
        
        Returns:
            Dict containing model statistics
        """
        try:
            if self.model is None or self.trainset is None:
                return {"error": "No model trained"}
            
            stats = {
                "model_type": type(self.model).__name__,
                "n_users": self.trainset.n_users,
                "n_items": self.trainset.n_items,
                "n_ratings": len(self.trainset.all_ratings()),
                "rating_scale": self.trainset.rating_scale,
                "global_mean": float(self.trainset.global_mean),
                "sparsity": 1 - (len(self.trainset.all_ratings()) / (self.trainset.n_users * self.trainset.n_items))
            }
            
            # Add algorithm-specific stats
            if hasattr(self.model, 'n_factors'):
                stats["n_factors"] = self.model.n_factors
            if hasattr(self.model, 'n_epochs'):
                stats["n_epochs"] = self.model.n_epochs
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting model stats: {str(e)}")
            return {"error": str(e)}
