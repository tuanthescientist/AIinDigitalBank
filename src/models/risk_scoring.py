"""
Risk Scoring Model
Credit risk assessment
"""

import numpy as np
from typing import Dict, List
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib


class RiskScoringModel:
    """Risk Scoring and Credit Assessment"""
    
    RISK_LEVELS = {
        'A': (0.00, 0.05, 'Excellent'),
        'B': (0.05, 0.15, 'Good'),
        'C': (0.15, 0.30, 'Fair'),
        'D': (0.30, 1.00, 'Poor')
    }
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.lr_model = None
        self.rf_model = None
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> Dict:
        """Train risk scoring model"""
        
        self.feature_names = feature_names
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Logistic Regression (interpretability)
        self.lr_model = LogisticRegression(
            C=1.0,
            max_iter=1000,
            class_weight='balanced',
            random_state=self.random_state
        )
        self.lr_model.fit(X_scaled, y)
        
        # Random Forest (feature importance)
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=self.random_state,
            class_weight='balanced'
        )
        self.rf_model.fit(X, y)
        
        # Training accuracy
        train_score_lr = self.lr_model.score(X_scaled, y)
        train_score_rf = self.rf_model.score(X, y)
        
        return {
            'status': 'trained',
            'lr_accuracy': train_score_lr,
            'rf_accuracy': train_score_rf,
            'n_features': len(feature_names)
        }
    
    def predict_risk_score(self, X: np.ndarray) -> np.ndarray:
        """
        Predict risk score (default probability)
        Ensemble of LR and RF models
        """
        if self.lr_model is None or self.rf_model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X_scaled = self.scaler.transform(X)
        
        # Ensemble prediction: 60% LR, 40% RF
        lr_proba = self.lr_model.predict_proba(X_scaled)[:, 1]
        rf_proba = self.rf_model.predict_proba(X)[:, 1]
        
        ensemble_score = 0.6 * lr_proba + 0.4 * rf_proba
        
        return ensemble_score
    
    def predict_with_decisions(self, X: np.ndarray) -> List[Dict]:
        """Predict risk with credit decision"""
        
        scores = self.predict_risk_score(X)
        
        results = []
        for score in scores:
            risk_level = self._score_to_level(score)
            decision = self._get_decision(risk_level)
            conditions = self._get_conditions(risk_level)
            
            results.append({
                'risk_score': float(score),
                'risk_level': risk_level,
                'default_probability': float(score),
                'decision': decision,
                'conditions': conditions
            })
        
        return results
    
    def _score_to_level(self, score: float) -> str:
        """Convert score to risk level"""
        for level, (min_s, max_s, desc) in self.RISK_LEVELS.items():
            if min_s <= score < max_s:
                return level
        return 'D'
    
    def _get_decision(self, risk_level: str) -> str:
        """Get credit decision based on risk level"""
        decisions = {
            'A': 'APPROVE',
            'B': 'APPROVE_WITH_CONDITIONS',
            'C': 'MANUAL_REVIEW',
            'D': 'REJECT'
        }
        return decisions.get(risk_level, 'REJECT')
    
    def _get_conditions(self, risk_level: str) -> List[str]:
        """Get lending conditions based on risk level"""
        conditions_map = {
            'A': ['Standard terms', 'Market rate pricing'],
            'B': ['Higher interest rate (prime + 1%)', 'Stricter covenants'],
            'C': ['Manual underwriting required', 'Lower credit limit'],
            'D': ['Reject or require collateral', 'Consider alternative products']
        }
        return conditions_map.get(risk_level, [])
    
    def get_top_risk_factors(self, X: np.ndarray, n: int = 10) -> Dict:
        """Get top n risk factors from RF model"""
        importances = self.rf_model.feature_importances_
        indices = np.argsort(importances)[::-1][:n]
        
        return {
            self.feature_names[i]: float(importances[i])
            for i in indices
        }
    
    def save(self, path: str):
        """Save model to disk"""
        joblib.dump({
            'lr_model': self.lr_model,
            'rf_model': self.rf_model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, path)
    
    def load(self, path: str):
        """Load model from disk"""
        data = joblib.load(path)
        self.lr_model = data['lr_model']
        self.rf_model = data['rf_model']
        self.scaler = data['scaler']
        self.feature_names = data['feature_names']
