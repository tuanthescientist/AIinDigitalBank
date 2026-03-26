"""
Customer Segmentation Model
Implements K-Means clustering for customer segmentation
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import joblib


class CustomerSegmentationModel:
    """Customer Segmentation using K-Means"""
    
    SEGMENTS = {
        0: 'VIP_INVESTORS',
        1: 'GROWING_PROFESSIONALS',
        2: 'CONSERVATIVE_SAVERS',
        3: 'EMERGING_CUSTOMERS',
        4: 'AT_RISK',
        5: 'DORMANT'
    }
    
    def __init__(self, n_clusters: int = 6, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.feature_names = None
    
    def train(self, X: np.ndarray, feature_names: List[str]) -> Dict:
        """Train segmentation model"""
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train K-Means
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )
        clusters = self.model.fit_predict(X_scaled)
        
        # Calculate metrics
        silhouette = silhouette_score(X_scaled, clusters)
        inertia = self.model.inertia_
        
        self.feature_names = feature_names
        
        return {
            'silhouette_score': silhouette,
            'inertia': inertia,
            'n_clusters': self.n_clusters,
            'status': 'trained'
        }
    
    def predict(self, X: np.ndarray) -> List[int]:
        """Predict customer segment"""
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def predict_with_names(self, X: np.ndarray) -> List[str]:
        """Predict customer segment with segment names"""
        clusters = self.predict(X)
        return [self.SEGMENTS.get(c, 'UNKNOWN') for c in clusters]
    
    def get_segment_profiles(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Get profile statistics for each segment"""
        profiles = {}
        
        for segment_id in range(self.n_clusters):
            mask = y == segment_id
            segment_data = X[mask]
            
            profiles[self.SEGMENTS[segment_id]] = {
                'count': int(np.sum(mask)),
                'percentage': float(np.sum(mask) / len(y) * 100),
                'mean_values': {
                    fname: float(val) 
                    for fname, val in zip(self.feature_names, np.mean(segment_data, axis=0))
                }
            }
        
        return profiles
    
    def save(self, path: str):
        """Save model to disk"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, path)
    
    def load(self, path: str):
        """Load model from disk"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_names = data['feature_names']
