"""
Unit tests for ML models
"""

import unittest
import numpy as np
from src.models import (
    CustomerSegmentationModel,
    ChurnPredictionModel,
    RecommendationEngine,
    RiskScoringModel
)


class TestCustomerSegmentation(unittest.TestCase):
    """Test customer segmentation model"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.model = CustomerSegmentationModel(n_clusters=3)
        # Generate dummy data
        self.X = np.random.rand(100, 5)
        self.feature_names = ['feat1', 'feat2', 'feat3', 'feat4', 'feat5']
    
    def test_training(self):
        """Test model training"""
        result = self.model.train(self.X, self.feature_names)
        self.assertEqual(result['status'], 'trained')
        self.assertGreater(result['silhouette_score'], 0)
    
    def test_prediction(self):
        """Test model prediction"""
        self.model.train(self.X, self.feature_names)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.X))
        self.assertTrue(all(0 <= p < 3 for p in predictions))


class TestChurnPrediction(unittest.TestCase):
    """Test churn prediction model"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.model = ChurnPredictionModel()
        self.X = np.random.rand(100, 10)
        self.y = np.random.randint(0, 2, 100)
        self.feature_names = [f'feat{i}' for i in range(10)]
    
    def test_training(self):
        """Test model training"""
        result = self.model.train(self.X, self.y, self.feature_names)
        self.assertEqual(result['status'], 'trained')
        self.assertGreater(result['accuracy'], 0)
    
    def test_prediction(self):
        """Test model prediction"""
        self.model.train(self.X, self.y, self.feature_names)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.X))
        self.assertTrue(all(0 <= p <= 1 for p in predictions))


class TestRiskScoring(unittest.TestCase):
    """Test risk scoring model"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.model = RiskScoringModel()
        self.X = np.random.rand(100, 15)
        self.y = np.random.randint(0, 2, 100)
        self.feature_names = [f'feat{i}' for i in range(15)]
    
    def test_training(self):
        """Test model training"""
        result = self.model.train(self.X, self.y, self.feature_names)
        self.assertEqual(result['status'], 'trained')
    
    def test_prediction(self):
        """Test model prediction"""
        self.model.train(self.X, self.y, self.feature_names)
        predictions = self.model.predict_risk_score(self.X)
        self.assertEqual(len(predictions), len(self.X))


if __name__ == '__main__':
    unittest.main()
