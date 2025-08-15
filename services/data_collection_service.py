"""
Data Collection Service for AI Features
Handles collection of user interaction data, product data, and analytics for AI training
"""
import pandas as pd
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from config import Config
import os

logger = logging.getLogger(__name__)

class DataCollectionService:
    """Service for collecting and managing data for AI features"""
    
    def __init__(self, db_path: str = "ai_data_collection.db"):
        """Initialize data collection service"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for data collection"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # User interactions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        session_id TEXT,
                        product_id TEXT NOT NULL,
                        interaction_type TEXT NOT NULL,
                        interaction_value REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                # Product views table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS product_views (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        product_id TEXT NOT NULL,
                        view_duration INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        referrer TEXT,
                        user_agent TEXT
                    )
                """)
                
                # Purchase history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS purchase_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        product_id TEXT NOT NULL,
                        quantity INTEGER DEFAULT 1,
                        price REAL NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        order_id TEXT
                    )
                """)
                
                # Product ratings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS product_ratings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        product_id TEXT NOT NULL,
                        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                        review_text TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Search queries table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS search_queries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        query TEXT NOT NULL,
                        results_count INTEGER,
                        clicked_results TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # AI generated content performance
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ai_content_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id TEXT NOT NULL,
                        content_type TEXT NOT NULL,
                        generated_content TEXT NOT NULL,
                        performance_metrics TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    def track_user_interaction(self, user_id: str, product_id: str, 
                             interaction_type: str, interaction_value: float = None,
                             session_id: str = None, metadata: Dict = None) -> bool:
        """
        Track user interaction with products
        
        Args:
            user_id: User identifier
            product_id: Product identifier  
            interaction_type: Type of interaction (view, click, add_to_cart, purchase, rating)
            interaction_value: Numerical value (rating, price, duration)
            session_id: Session identifier
            metadata: Additional metadata
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_interactions 
                    (user_id, product_id, interaction_type, interaction_value, session_id, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, product_id, interaction_type, interaction_value, 
                      session_id, json.dumps(metadata) if metadata else None))
                conn.commit()
                
            logger.debug(f"Tracked interaction: {interaction_type} for user {user_id} on product {product_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error tracking user interaction: {str(e)}")
            return False

    def track_product_view(self, product_id: str, user_id: str = None, 
                          view_duration: int = None, referrer: str = None,
                          user_agent: str = None) -> bool:
        """Track product page views"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO product_views 
                    (user_id, product_id, view_duration, referrer, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, product_id, view_duration, referrer, user_agent))
                conn.commit()
                
            return True
            
        except Exception as e:
            logger.error(f"Error tracking product view: {str(e)}")
            return False

    def track_purchase(self, user_id: str, product_id: str, quantity: int = 1,
                      price: float = 0, order_id: str = None) -> bool:
        """Track product purchases"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO purchase_history 
                    (user_id, product_id, quantity, price, order_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, product_id, quantity, price, order_id))
                conn.commit()
                
            # Also track as interaction
            self.track_user_interaction(user_id, product_id, "purchase", price)
            
            return True
            
        except Exception as e:
            logger.error(f"Error tracking purchase: {str(e)}")
            return False

    def track_rating(self, user_id: str, product_id: str, rating: int,
                    review_text: str = None) -> bool:
        """Track product ratings and reviews"""
        try:
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
                
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO product_ratings 
                    (user_id, product_id, rating, review_text)
                    VALUES (?, ?, ?, ?)
                """, (user_id, product_id, rating, review_text))
                conn.commit()
                
            # Also track as interaction
            self.track_user_interaction(user_id, product_id, "rating", float(rating))
            
            return True
            
        except Exception as e:
            logger.error(f"Error tracking rating: {str(e)}")
            return False

    def track_search_query(self, query: str, user_id: str = None,
                          results_count: int = None, 
                          clicked_results: List[str] = None) -> bool:
        """Track search queries and results"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO search_queries 
                    (user_id, query, results_count, clicked_results)
                    VALUES (?, ?, ?, ?)
                """, (user_id, query, results_count, 
                      json.dumps(clicked_results) if clicked_results else None))
                conn.commit()
                
            return True
            
        except Exception as e:
            logger.error(f"Error tracking search query: {str(e)}")
            return False

    def track_ai_content_performance(self, product_id: str, content_type: str,
                                   generated_content: str, 
                                   performance_metrics: Dict = None) -> bool:
        """Track performance of AI-generated content"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO ai_content_performance 
                    (product_id, content_type, generated_content, performance_metrics)
                    VALUES (?, ?, ?, ?)
                """, (product_id, content_type, generated_content,
                      json.dumps(performance_metrics) if performance_metrics else None))
                conn.commit()
                
            return True
            
        except Exception as e:
            logger.error(f"Error tracking AI content performance: {str(e)}")
            return False

    def get_user_interaction_history(self, user_id: str, 
                                   days_back: int = 30) -> pd.DataFrame:
        """Get user interaction history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT * FROM user_interactions 
                    WHERE user_id = ? 
                    AND timestamp >= datetime('now', '-{} days')
                    ORDER BY timestamp DESC
                """.format(days_back)
                
                df = pd.read_sql_query(query, conn, params=[user_id])
                return df
                
        except Exception as e:
            logger.error(f"Error getting user interaction history: {str(e)}")
            return pd.DataFrame()

    def get_ratings_data_for_ml(self) -> pd.DataFrame:
        """Get ratings data formatted for machine learning"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT user_id, product_id, rating
                    FROM product_ratings 
                    WHERE rating IS NOT NULL
                """
                df = pd.read_sql_query(query, conn)
                return df
                
        except Exception as e:
            logger.error(f"Error getting ratings data: {str(e)}")
            return pd.DataFrame()

    def get_product_popularity_metrics(self) -> Dict[str, Any]:
        """Get product popularity metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Most viewed products
                most_viewed = pd.read_sql_query("""
                    SELECT product_id, COUNT(*) as view_count
                    FROM product_views
                    GROUP BY product_id
                    ORDER BY view_count DESC
                    LIMIT 20
                """, conn)
                
                # Most purchased products
                most_purchased = pd.read_sql_query("""
                    SELECT product_id, COUNT(*) as purchase_count, SUM(quantity) as total_quantity
                    FROM purchase_history
                    GROUP BY product_id
                    ORDER BY purchase_count DESC
                    LIMIT 20
                """, conn)
                
                # Highest rated products
                highest_rated = pd.read_sql_query("""
                    SELECT product_id, AVG(rating) as avg_rating, COUNT(*) as rating_count
                    FROM product_ratings
                    GROUP BY product_id
                    HAVING rating_count >= 5
                    ORDER BY avg_rating DESC
                    LIMIT 20
                """, conn)
                
                return {
                    "most_viewed": most_viewed.to_dict('records'),
                    "most_purchased": most_purchased.to_dict('records'),
                    "highest_rated": highest_rated.to_dict('records')
                }
                
        except Exception as e:
            logger.error(f"Error getting popularity metrics: {str(e)}")
            return {}

    def get_user_behavior_insights(self) -> Dict[str, Any]:
        """Get insights about user behavior patterns"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Active users
                active_users = pd.read_sql_query("""
                    SELECT COUNT(DISTINCT user_id) as active_users
                    FROM user_interactions
                    WHERE timestamp >= datetime('now', '-7 days')
                """, conn)
                
                # Interaction patterns
                interaction_patterns = pd.read_sql_query("""
                    SELECT interaction_type, COUNT(*) as count
                    FROM user_interactions
                    WHERE timestamp >= datetime('now', '-30 days')
                    GROUP BY interaction_type
                    ORDER BY count DESC
                """, conn)
                
                # Average session metrics
                session_metrics = pd.read_sql_query("""
                    SELECT 
                        AVG(view_duration) as avg_view_duration,
                        COUNT(*) as total_views
                    FROM product_views
                    WHERE view_duration IS NOT NULL
                    AND timestamp >= datetime('now', '-30 days')
                """, conn)
                
                return {
                    "active_users": active_users.iloc[0]['active_users'] if not active_users.empty else 0,
                    "interaction_patterns": interaction_patterns.to_dict('records'),
                    "avg_view_duration": session_metrics.iloc[0]['avg_view_duration'] if not session_metrics.empty else 0,
                    "total_views": session_metrics.iloc[0]['total_views'] if not session_metrics.empty else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting user behavior insights: {str(e)}")
            return {}

    def export_data_for_training(self, output_dir: str = "training_data") -> Dict[str, str]:
        """Export collected data for AI model training"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            exported_files = {}
            
            with sqlite3.connect(self.db_path) as conn:
                # Export ratings data
                ratings_df = pd.read_sql_query("""
                    SELECT user_id, product_id, rating, timestamp
                    FROM product_ratings
                """, conn)
                ratings_file = os.path.join(output_dir, "ratings_data.csv")
                ratings_df.to_csv(ratings_file, index=False)
                exported_files["ratings"] = ratings_file
                
                # Export interaction data
                interactions_df = pd.read_sql_query("""
                    SELECT user_id, product_id, interaction_type, interaction_value, timestamp
                    FROM user_interactions
                """, conn)
                interactions_file = os.path.join(output_dir, "interactions_data.csv")
                interactions_df.to_csv(interactions_file, index=False)
                exported_files["interactions"] = interactions_file
                
                # Export product views
                views_df = pd.read_sql_query("""
                    SELECT user_id, product_id, view_duration, timestamp
                    FROM product_views
                """, conn)
                views_file = os.path.join(output_dir, "product_views.csv")
                views_df.to_csv(views_file, index=False)
                exported_files["views"] = views_file
                
                # Export purchase history
                purchases_df = pd.read_sql_query("""
                    SELECT user_id, product_id, quantity, price, timestamp
                    FROM purchase_history
                """, conn)
                purchases_file = os.path.join(output_dir, "purchase_history.csv")
                purchases_df.to_csv(purchases_file, index=False)
                exported_files["purchases"] = purchases_file
            
            logger.info(f"Data exported to {output_dir}")
            return exported_files
            
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return {}

    def get_data_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about collected data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                stats = {}
                
                # Count records in each table
                tables = [
                    'user_interactions', 'product_views', 'purchase_history', 
                    'product_ratings', 'search_queries', 'ai_content_performance'
                ]
                
                for table in tables:
                    count_df = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn)
                    stats[table] = count_df.iloc[0]['count']
                
                # Get date range of collected data
                date_range_df = pd.read_sql_query("""
                    SELECT 
                        MIN(timestamp) as earliest_data,
                        MAX(timestamp) as latest_data
                    FROM user_interactions
                """, conn)
                
                if not date_range_df.empty:
                    stats['data_range'] = {
                        'earliest': date_range_df.iloc[0]['earliest_data'],
                        'latest': date_range_df.iloc[0]['latest_data']
                    }
                
                # Unique users and products
                unique_df = pd.read_sql_query("""
                    SELECT 
                        COUNT(DISTINCT user_id) as unique_users,
                        COUNT(DISTINCT product_id) as unique_products
                    FROM user_interactions
                """, conn)
                
                if not unique_df.empty:
                    stats['unique_users'] = unique_df.iloc[0]['unique_users']
                    stats['unique_products'] = unique_df.iloc[0]['unique_products']
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting data collection stats: {str(e)}")
            return {}
