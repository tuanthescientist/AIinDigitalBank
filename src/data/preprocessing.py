"""
Data Ingestion Module
Handles data loading and preprocessing
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple


class DataIngestion:
    """Data ingestion and loading"""
    
    @staticmethod
    def load_customer_data(file_path: str) -> pd.DataFrame:
        """Load customer data from CSV"""
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
    
    @staticmethod
    def load_transaction_data(file_path: str) -> pd.DataFrame:
        """Load transaction data from CSV"""
        try:
            df = pd.read_csv(file_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
    
    @staticmethod
    def load_events_data(file_path: str) -> pd.DataFrame:
        """Load customer events data"""
        try:
            df = pd.read_csv(file_path)
            df['created_at'] = pd.to_datetime(df['created_at'])
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")


class DataPreprocessing:
    """Data cleaning and preprocessing"""
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """Handle missing values"""
        if strategy == 'mean':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'forward_fill':
            df = df.fillna(method='ffill')
        
        return df
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """Remove duplicate rows"""
        return df.drop_duplicates(subset=subset)
    
    @staticmethod
    def normalize_features(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Normalize numeric features (0-1 scaling)"""
        df_norm = df.copy()
        
        for col in columns:
            if col in df_norm.columns:
                min_val = df_norm[col].min()
                max_val = df_norm[col].max()
                
                if max_val > min_val:
                    df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
        
        return df_norm


class FeatureEngineering:
    """Feature creation and transformation"""
    
    @staticmethod
    def create_customer_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create customer-level features"""
        features = df.copy()
        
        # Account age in days (assuming 'created_at' exists)
        if 'created_at' in features.columns:
            features['created_at'] = pd.to_datetime(features['created_at'])
            features['account_age_days'] = (pd.Timestamp.now() - features['created_at']).dt.days
        
        return features
    
    @staticmethod
    def create_behavioral_features(events_df: pd.DataFrame) -> pd.DataFrame:
        """Create behavioral features from events"""
        
        # Group by customer
        features = []
        
        for cust_id, group in events_df.groupby('customer_id'):
            # Last 30 days
            thirty_days_ago = pd.Timestamp.now() - pd.Timedelta(days=30)
            recent_events = group[group['created_at'] >= thirty_days_ago]
            
            feature_dict = {
                'customer_id': cust_id,
                'event_count_30d': len(recent_events),
                'unique_event_types': recent_events['event_type'].nunique(),
            }
            
            features.append(feature_dict)
        
        return pd.DataFrame(features)
