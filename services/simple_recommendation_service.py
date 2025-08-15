"""
Simple Product Recommendation Service
Handles personalized recommendations using scikit-learn for collaborative filtering
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

class SimpleRecommendationService:
    """Simple service class for product recommendation operations using scikit-learn"""
    
    def __init__(self):
        """Initialize recommendation service"""
        self.model = None
        self.user_item_matrix = None
        self.item_features = {}
        self.user_features = {}
        self.model_path = "simple_recommendation_model.pkl"
        self.ratings_df = None
        
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
            self.ratings_df = ratings_df
            
            # Create user-item matrix for analysis
            self.user_item_matrix = ratings_df.pivot(index='user_id', columns='product_id', values='rating').fillna(0)
            
            logger.info(f"Data prepared: {len(ratings_df)} ratings, {ratings_df['user_id'].nunique()} users, {ratings_df['product_id'].nunique()} items")
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
    
    def train_model(self, algorithm: str = "NMF") -> Dict[str, Any]:
        """
        Train recommendation model
        
        Args:
            algorithm: Algorithm to use ("NMF")
            
        Returns:
            Dict containing training results
        """
        try:
            if self.user_item_matrix is None:
                raise ValueError("Data not prepared. Call prepare_data() first.")
            
            # Use NMF (Non-negative Matrix Factorization) for collaborative filtering
            if algorithm == "NMF":
                self.model = NMF(n_components=10, random_state=42, max_iter=200)
                # Fit the model on the user-item matrix
                user_factors = self.model.fit_transform(self.user_item_matrix)
                item_factors = self.model.components_
                
                # Store factors for later use
                self.user_factors = user_factors
                self.item_factors = item_factors
                
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
            
            # Calculate some basic metrics
            n_users = self.user_item_matrix.shape[0]
            n_items = self.user_item_matrix.shape[1]
            n_ratings = np.count_nonzero(self.user_item_matrix.values)
            sparsity = 1 - (n_ratings / (n_users * n_items))
            
            results = {
                "algorithm": algorithm,
                "n_users": n_users,
                "n_items": n_items,
                "n_ratings": n_ratings,
                "sparsity": float(sparsity),
                "trained_at": "2025-08-14T19:43:23Z"
            }
            
            logger.info(f"Model trained successfully with {algorithm}")
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
                'user_item_matrix': self.user_item_matrix,
                'user_factors': getattr(self, 'user_factors', None),
                'item_factors': getattr(self, 'item_factors', None),
                'ratings_df': self.ratings_df,
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
            self.user_item_matrix = model_data.get('user_item_matrix')
            self.user_factors = model_data.get('user_factors')
            self.item_factors = model_data.get('item_factors')
            self.ratings_df = model_data.get('ratings_df')
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
            if self.model is None or self.user_item_matrix is None:
                raise ValueError("Model not trained. Train or load a model first.")
            
            if user_id not in self.user_item_matrix.index:
                # New user - return popular items
                return self.get_popular_items(n_recommendations)
            
            user_idx = self.user_item_matrix.index.get_loc(user_id)
            
            # Get user's rated items if excluding them
            rated_items = set()
            if exclude_rated:
                user_ratings = self.user_item_matrix.loc[user_id]
                rated_items = set(user_ratings[user_ratings > 0].index)
            
            # Get predictions using matrix factorization
            if hasattr(self, 'user_factors') and hasattr(self, 'item_factors'):
                user_vector = self.user_factors[user_idx]
                predicted_ratings = np.dot(user_vector, self.item_factors)
                
                predictions = []
                for i, (product_id, predicted_rating) in enumerate(zip(self.user_item_matrix.columns, predicted_ratings)):
                    if exclude_rated and product_id in rated_items:
                        continue
                    
                    predictions.append({
                        'product_id': product_id,
                        'predicted_rating': float(predicted_rating),
                        'confidence': min(float(predicted_rating) / 5.0, 1.0)
                    })
                
                # Sort by predicted rating and take top N
                predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
                top_recommendations = predictions[:n_recommendations]
            else:
                # Fallback to similarity-based recommendations
                top_recommendations = []
            
            result = {
                "user_id": user_id,
                "recommendations": top_recommendations,
                "total_available": len(predictions) if 'predictions' in locals() else 0,
                "excluded_rated_items": len(rated_items) if exclude_rated else 0,
                "generated_at": "2025-08-14T19:43:23Z"
            }
            
            logger.info(f"Generated {len(top_recommendations)} recommendations for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting user recommendations: {str(e)}")
            return {"error": str(e)}
    
    def get_item_recommendations(self, item_id: str, n_recommendations: int = 10) -> Dict[str, Any]:
        """
        Get similar item recommendations using cosine similarity
        
        Args:
            item_id: Item ID to find similar items for
            n_recommendations: Number of similar items to return
            
        Returns:
            Dict containing similar items
        """
        try:
            if self.user_item_matrix is None:
                raise ValueError("Model not trained. Train or load a model first.")
            
            if item_id not in self.user_item_matrix.columns:
                return {"error": f"Item {item_id} not found in training data"}
            
            # Get item vectors (transpose to get item profiles)
            item_profiles = self.user_item_matrix.T
            
            # Calculate cosine similarity between items
            item_similarities = cosine_similarity(item_profiles.values)
            item_idx = item_profiles.index.get_loc(item_id)
            
            # Get similarities for target item
            similarities = item_similarities[item_idx]
            
            # Create list of similar items
            similar_items = []
            for i, (other_item_id, similarity_score) in enumerate(zip(item_profiles.index, similarities)):
                if other_item_id == item_id:
                    continue
                
                similar_items.append({
                    'product_id': other_item_id,
                    'similarity_score': float(similarity_score),
                    'confidence': float(abs(similarity_score))
                })
            
            # Sort by similarity and take top N
            similar_items.sort(key=lambda x: x['similarity_score'], reverse=True)
            top_similar = similar_items[:n_recommendations]
            
            result = {
                "item_id": item_id,
                "similar_items": top_similar,
                "total_available": len(similar_items),
                "generated_at": "2025-08-14T19:43:23Z"
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
                "generated_at": "2025-08-14T19:43:23Z"
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
            if self.model is None or self.user_item_matrix is None:
                raise ValueError("Model not trained. Train or load a model first.")
            
            if user_id not in self.user_item_matrix.index:
                # New user - return average rating for item
                if item_id in self.user_item_matrix.columns:
                    item_ratings = self.user_item_matrix[item_id]
                    avg_rating = item_ratings[item_ratings > 0].mean()
                    predicted_rating = avg_rating if not np.isnan(avg_rating) else 3.0
                else:
                    predicted_rating = 3.0  # Default rating
                was_impossible = True
            elif item_id not in self.user_item_matrix.columns:
                # New item - return user's average rating
                user_ratings = self.user_item_matrix.loc[user_id]
                avg_rating = user_ratings[user_ratings > 0].mean()
                predicted_rating = avg_rating if not np.isnan(avg_rating) else 3.0
                was_impossible = True
            else:
                # Both user and item exist
                if hasattr(self, 'user_factors') and hasattr(self, 'item_factors'):
                    user_idx = self.user_item_matrix.index.get_loc(user_id)
                    item_idx = self.user_item_matrix.columns.get_loc(item_id)
                    
                    user_vector = self.user_factors[user_idx]
                    item_vector = self.item_factors[:, item_idx]
                    
                    predicted_rating = float(np.dot(user_vector, item_vector))
                    was_impossible = False
                else:
                    predicted_rating = 3.0
                    was_impossible = True
            
            # Ensure rating is within valid range
            predicted_rating = max(1.0, min(5.0, predicted_rating))
            
            result = {
                "user_id": user_id,
                "item_id": item_id,
                "predicted_rating": float(predicted_rating),
                "was_impossible": was_impossible,
                "confidence": 1 - abs(predicted_rating - round(predicted_rating)),
                "generated_at": "2025-08-14T19:43:23Z"
            }
            
            logger.info(f"Predicted rating: {predicted_rating:.2f} for user {user_id}, item {item_id}")
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
            if self.model is None or self.user_item_matrix is None:
                return {"error": "No model trained"}
            
            n_users = self.user_item_matrix.shape[0]
            n_items = self.user_item_matrix.shape[1]
            n_ratings = np.count_nonzero(self.user_item_matrix.values)
            
            stats = {
                "model_type": type(self.model).__name__,
                "n_users": n_users,
                "n_items": n_items,
                "n_ratings": n_ratings,
                "rating_scale": (1, 5),
                "global_mean": float(self.user_item_matrix.values[self.user_item_matrix.values > 0].mean()),
                "sparsity": 1 - (n_ratings / (n_users * n_items))
            }
            
            # Add algorithm-specific stats
            if hasattr(self.model, 'n_components'):
                stats["n_components"] = self.model.n_components
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting model stats: {str(e)}")
            return {"error": str(e)}
