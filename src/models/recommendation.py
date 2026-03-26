"""
Product Recommendation Engine
Hybrid recommendation system (Collaborative + Content-based)
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class RecommendationEngine:
    """Product Recommendation Engine"""
    
    def __init__(self, fallback_popularity: bool = True):
        self.fallback_popularity = fallback_popularity
        self.customer_features = None
        self.product_features = None
        self.interaction_matrix = None
        self.popularities = None
    
    def fit(
        self,
        customer_features: np.ndarray,
        product_features: np.ndarray,
        interaction_matrix: np.ndarray,
        customer_ids: List[str],
        product_ids: List[str]
    ):
        """Fit recommendation model"""
        
        self.customer_features = customer_features
        self.product_features = product_features
        self.interaction_matrix = interaction_matrix
        self.customer_ids = customer_ids
        self.product_ids = product_ids
        
        # Calculate product popularity
        self.popularities = np.mean(interaction_matrix, axis=0)
    
    def recommend(
        self,
        customer_id: str,
        n_recommendations: int = 5,
        method: str = 'hybrid'
    ) -> List[Dict]:
        """
        Generate recommendations for a customer
        
        Args:
            customer_id: Customer identifier
            n_recommendations: Number of recommendations
            method: 'collaborative', 'content', or 'hybrid'
        
        Returns:
            List of recommendations with scores
        """
        
        if customer_id not in self.customer_ids:
            # Fallback to popular products
            return self._get_popular_products(n_recommendations)
        
        customer_idx = self.customer_ids.index(customer_id)
        
        if method == 'collaborative':
            scores = self._collaborative_filtering(customer_idx)
        elif method == 'content':
            scores = self._content_based(customer_idx)
        else:  # hybrid
            scores = self._hybrid_recommendation(customer_idx)
        
        # Get top recommendations
        top_indices = np.argsort(scores)[::-1][:n_recommendations]
        
        recommendations = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only positive scores
                recommendations.append({
                    'product_id': self.product_ids[idx],
                    'score': float(scores[idx]),
                    'rank': len(recommendations) + 1
                })
        
        return recommendations
    
    def _collaborative_filtering(self, customer_idx: int) -> np.ndarray:
        """Collaborative filtering score"""
        
        # User-user similarity
        customer_similarity = cosine_similarity(
            self.customer_features[customer_idx:customer_idx+1],
            self.customer_features
        )[0]
        
        # Find similar customers
        similar_customers_idx = np.argsort(customer_similarity)[::-1][1:11]  # Top 10
        
        # Aggregate their preferences
        scores = np.mean(
            self.interaction_matrix[similar_customers_idx],
            axis=0
        )
        
        # Exclude already purchased
        scores[self.interaction_matrix[customer_idx] > 0] = 0
        
        return scores
    
    def _content_based(self, customer_idx: int) -> np.ndarray:
        """Content-based recommendation score"""
        
        # Similarity between customer and products
        scores = cosine_similarity(
            self.customer_features[customer_idx:customer_idx+1],
            self.product_features
        )[0]
        
        # Exclude already purchased
        scores[self.interaction_matrix[customer_idx] > 0] = 0
        
        return scores
    
    def _hybrid_recommendation(self, customer_idx: int) -> np.ndarray:
        """Hybrid recommendation (collaborative + content)"""
        
        cf_scores = self._collaborative_filtering(customer_idx)
        cb_scores = self._content_based(customer_idx)
        popularity_scores = self.popularities / np.max(self.popularities)
        
        # Weighted combination
        hybrid_scores = (
            0.35 * cf_scores +
            0.35 * cb_scores +
            0.30 * popularity_scores
        )
        
        return hybrid_scores
    
    def _get_popular_products(self, n: int) -> List[Dict]:
        """Fallback to most popular products"""
        top_indices = np.argsort(self.popularities)[::-1][:n]
        
        return [
            {
                'product_id': self.product_ids[idx],
                'score': float(self.popularities[idx]),
                'rank': i + 1
            }
            for i, idx in enumerate(top_indices)
        ]
    
    def explain_recommendation(self, customer_id: str, product_id: str) -> Dict:
        """Explain why a product was recommended"""
        
        customer_idx = self.customer_ids.index(customer_id)
        product_idx = self.product_ids.index(product_id)
        
        cf_sim = cosine_similarity(
            self.customer_features[customer_idx:customer_idx+1],
            self.customer_features
        )[0]
        
        cb_sim = cosine_similarity(
            self.customer_features[customer_idx:customer_idx+1],
            self.product_features
        )[0][product_idx]
        
        popularity = self.popularities[product_idx]
        
        return {
            'collaborative_score': float(cf_sim.mean()),
            'content_score': float(cb_sim),
            'popularity_score': float(popularity),
            'reason': self._generate_reason(cf_sim.mean(), cb_sim, popularity)
        }
    
    def _generate_reason(self, cf: float, cb: float, pop: float) -> str:
        """Generate human-readable explanation"""
        
        if cf > 0.7:
            return "Popular among customers like you"
        elif cb > 0.7:
            return "Matches your profile and preferences"
        elif pop > 0.6:
            return "Popular product in your segment"
        else:
            return "Recommended based on your interests"
