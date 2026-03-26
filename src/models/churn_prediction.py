"""
Churn Prediction Model
Binary classification using LightGBM
"""

import numpy as np
from typing import Dict, List
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
import joblib


class ChurnPredictionModel:
    """Churn Prediction using LightGBM"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.feature_names = None
        self.scaler = StandardScaler()
    
    def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> Dict:
        """Train churn prediction model"""
        
        self.feature_names = feature_names
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Create and train model
        self.model = lgb.LGBMClassifier(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=7,
            num_leaves=31,
            min_child_samples=20,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=self.random_state,
            class_weight='balanced',
            verbose=-1
        )
        
        self.model.fit(X_scaled, y)
        
        # Calculate feature importance
        importance = dict(zip(feature_names, self.model.feature_importances_))
        
        # Training accuracy
        train_score = self.model.score(X_scaled, y)
        
        return {
            'status': 'trained',
            'accuracy': train_score,
            'n_features': len(feature_names),
            'feature_importance': importance
        }
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict churn probability (0-1)"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]
    
    def predict_with_risk_level(self, X: np.ndarray) -> List[Dict]:
        """Predict churn with risk level"""
        probabilities = self.predict(X)
        
        results = []
        for prob in probabilities:
            if prob > 0.7:
                risk_level = 'HIGH'
                intervention = 'URGENT'
            elif prob > 0.4:
                risk_level = 'MEDIUM'
                intervention = 'TARGETED'
            else:
                risk_level = 'LOW'
                intervention = 'STANDARD'
            
            results.append({
                'churn_probability': float(prob),
                'risk_level': risk_level,
                'intervention': intervention
            })
        
        return results
    
    def get_top_features(self, n: int = 10) -> Dict:
        """Get top n important features"""
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:n]
        
        return {
            self.feature_names[i]: float(importances[i]) 
            for i in indices
        }
    
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
