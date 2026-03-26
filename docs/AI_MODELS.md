# AI/ML Models Specification

## Overview

This document details all machine learning models, their algorithms, features, and implementation specifics.

---

## 1. Customer Segmentation Model

### Model Type: Unsupervised Learning (Clustering)

### Algorithm: K-Means Clustering

### Input Features
```python
features = [
    'account_age_days',           # Days since account opening
    'total_balance_normalized',   # Normalized account balance
    'transaction_count_30d',      # Transactions in 30 days
    'avg_transaction_amount',     # Average transaction value
    'product_count',              # Number of products
    'login_frequency_30d',        # Monthly logins
    'support_contacts_30d',       # Support interactions
    'product_usage_score',        # Product engagement score
    'digital_adoption_score',     # Mobile/web usage
    'risk_appetite_score'         # From questionnaire
]
```

### Output: Customer Segment (1-8)

### Training Process
```python
# Normalize features
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Determine optimal k (Elbow method + Silhouette)
inertias, silhouette_scores = [], []
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_normalized)
    inertias.append(km.inertia_)
    silhouette_scores.append(silhouette_score(X_normalized, km.labels_))

# Select optimal k
optimal_k = 6  # or determined by analysis
model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
segments = model.fit_predict(X_normalized)
```

### Expected Performance
- Silhouette Score: 0.65-0.75
- Davies-Bouldin Index: <1.5
- Calinski-Harabasz Index: >30

### Segment Profiles (Example)
| Segment | Name | % of Customer | Characteristics | Strategy |
|---------|------|---|---|---|
| 0 | VIP Investors | 5% | High balance, multiple products | Premium services |
| 1 | Growing Professionals | 20% | Growing balance, active usage | Growth products |
| 2 | Conservative Savers | 25% | Stable, low risk | Protective products |
| 3 | Emerging | 30% | New customers, exploratory | Education, entry products |
| 4 | At-Risk | 15% | Low activity | Retention campaigns |
| 5 | Dormant | 5% | Inactive | Win-back campaigns |

---

## 2. Product Recommendation Engine

### Model Type: Collaborative + Content-Based Hybrid

### Architecture
```
Input: Customer ID
   ↓
Customer Feature Vector (embedding)
   ↓
Product Feature Vector (embedding)
   ↓
Similarity Calculation
   ├─→ Collaborative: User-User, Item-Item similarity
   ├─→ Content-based: Feature matching
   ├─→ Business Rules: Constraints and preferences
   └─→ Popularity Score: Trending products
   ↓
Weighted Combination
   ↓
Top-K Recommendations with Scores
```

### Algorithm Components

#### A. Collaborative Filtering
```python
# Item-Item Similarity
from sklearn.metrics.pairwise import cosine_similarity
item_similarity = cosine_similarity(product_features)

# User-based neighborhood
user_neighborhood = user_similarity_matrix[customer_id].argsort()[-k_neighbors:]
recommendations_cf = aggregate_neighborhood_preferences(user_neighborhood)
```

#### B. Content-Based Filtering
```python
# Customer preference vector
customer_pref_vector = encode_customer_profile(customer_segment, risk_profile, income)

# Product feature vector
product_feature_vector = encode_product(product_type, risk_level, return_profile)

# Similarity score
cbf_score = cosine_similarity(customer_pref_vector, product_feature_vector)
```

#### C. Hybrid Scoring
```python
# Final recommendation score
recommendation_score = (
    0.35 * collaborative_score +      # Collaborative filtering
    0.30 * content_score +             # Content-based
    0.20 * popularity_score +          # Trending/popular products
    0.15 * business_rules_boost        # Business logic boosts
)
```

### Features Used

**Customer Features:**
- Risk profile (conservative/moderate/aggressive)
- Income level (quintile)
- Age group
- Product ownership (which products owned)
- Investment horizon
- Digital adoption level

**Product Features:**
- Product type (savings/bonds/real estate/investment)
- Expected return
- Risk level
- Minimum investment
- Liquidity score
- Fee structure
- Historical popularity

### Output
```python
[
    {
        "product_id": "prod_123",
        "product_name": "Corporate Bonds Fund",
        "score": 0.85,
        "reason": "Matches your risk profile and return expectations",
        "expected_return": 6.5,
        "risk_level": "MEDIUM"
    },
    {
        "product_id": "prod_234",
        "product_name": "Real Estate Investment Trust",
        "score": 0.78,
        "reason": "Popular among customers in your segment",
        "expected_return": 7.2,
        "risk_level": "MEDIUM"
    }
]
```

### Performance Metrics
- **Precision@5**: 80-85% (of top 5 recs, how many customer engages)
- **Recall@10**: 60-70% (of customer interests, how many shown)
- **nDCG (normalized DCG)**: 0.75-0.85 (ranking quality)
- **Click-through rate**: 8-12% (actual customer engagement)
- **Conversion rate**: 3-5% (of clicked, how many purchase)

---

## 3. Churn Prediction Model

### Model Type: Supervised Binary Classification

### Algorithm: Gradient Boosting (LightGBM)

### Features (20-30 selected)
```python
features = [
    # Activity Features
    'transaction_count_30d',
    'transaction_count_90d',
    'transaction_trend',              # Increasing/decreasing
    'days_since_last_transaction',
    'login_frequency_30d',
    'support_contact_frequency',
    
    # Account Features
    'account_age_days',
    'account_balance',
    'balance_trend',
    'product_count',
    'product_tenure',
    
    # Engagement Features
    'email_open_rate',
    'notification_interaction',
    'app_usage_minutes_30d',
    'feature_adoption_score',
    
    # Economic Features
    'monthly_income',
    'monthly_expense_trend',
    'fee_burden_ratio',
    'alternative_bank_score',         # External data
    
    # Behavioral Features
    'complaint_frequency',
    'complaint_resolution_time',
    'segment_churn_rate',
    'demographic_churn_propensity'
]
```

### Training Process
```python
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold

# Data preparation
X_train_processed = preprocess_features(X_train, feature_names)
y_train_rebalanced = handle_class_imbalance(y_train, method='smote')

# Model training with cross-validation
skf = StratifiedKFold(n_splits=5)
cv_scores = []

for train_idx, val_idx in skf.split(X_train_processed, y_train_rebalanced):
    X_tr, X_val = X_train_processed[train_idx], X_train_processed[val_idx]
    y_tr, y_val = y_train_rebalanced[train_idx], y_train_rebalanced[val_idx]
    
    model = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=7,
        num_leaves=31,
        min_child_samples=20,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    
    model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], early_stopping_rounds=10)
    cv_scores.append(model.score(X_val, y_val))

# Final model on full training set
final_model = lgb.LGBMClassifier(**best_params)
final_model.fit(X_train_processed, y_train_rebalanced)
```

### Output
```python
churn_score = 0.85  # 0-1, probability of churning
churn_risk_level = 'HIGH'  # LOW (0-0.3), MEDIUM (0.3-0.7), HIGH (0.7-1.0)
churn_drivers = [
    'No transactions in 60 days',
    'Below average app usage',
    'Multiple support complaints'
]
```

### Performance Metrics
- **AUC-ROC**: 0.82-0.88
- **Precision**: 0.70-0.80 (of predicted churners, how many actually churn)
- **Recall**: 0.65-0.75 (of actual churners, how many identified)
- **F1-Score**: 0.70-0.78
- **Early detection**: >30 days before actual churn

### Intervention Strategy
```python
if churn_score > 0.7:
    intervention = 'URGENT'
    actions = ['Direct call', 'Personalized offer', 'Loyalty bonus']
elif churn_score > 0.4:
    intervention = 'TARGETED'
    actions = ['Email campaign', 'App notification', 'Product offer']
else:
    intervention = 'STANDARD'
    actions = ['Newsletter', 'Standard recommendations']
```

---

## 4. Risk Assessment & Credit Scoring Model

### Model Type: Supervised Classification

### Algorithm: Logistic Regression + Random Forest

### Features (30-40 selected)
```python
features = [
    # Credit Features
    'credit_history_score',
    'payment_default_count',
    'payment_lateness_months',
    'debt_to_income_ratio',
    'credit_utilization_ratio',
    
    # Account Features
    'account_age_months',
    'account_balance',
    'savings_rate',
    'emergency_fund_ratio',
    
    # Employment Features
    'employment_tenure_years',
    'employment_type',
    'income_stability_score',
    'income_growth_trend',
    
    # Behavioral Features
    'transaction_regularity',
    'spending_pattern_stability',
    'investment_experience',
    'risk_questionnaire_score',
    
    # External Features
    'credit_bureau_score',
    'sanctions_check',
    'pep_check',
    'business_registration_status'
]
```

### Risk Levels & Thresholds
```python
class RiskLevel(Enum):
    A = (0.00, 0.05)      # Excellent (0-5% default prob)
    B = (0.05, 0.15)      # Good (5-15%)
    C = (0.15, 0.30)      # Fair (15-30%)
    D = (0.30, 1.00)      # Poor (>30%)

# Output
{
    'risk_score': 0.12,
    'risk_level': 'B',
    'default_probability': 0.12,
    'decision': 'APPROVE_WITH_CONDITIONS',
    'conditions': [
        'Higher interest rate (prime + 2%)',
        'Stricter covenants',
        'Lower credit limit'
    ]
}
```

### Model Training
```python
# Logistic Regression for interpretability
lr_model = LogisticRegression(C=1.0, max_iter=1000, class_weight='balanced')
lr_model.fit(X_train_scaled, y_train)

# Random Forest for feature importance
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10)
rf_model.fit(X_train, y_train)

# Ensemble prediction
predictions = 0.6 * lr_model.predict_proba(X_test)[:, 1] + \
              0.4 * rf_model.predict_proba(X_test)[:, 1]
```

### Performance Metrics
- **AUC-ROC**: 0.80-0.85
- **Accuracy**: 85-90%
- **Precision**: 75-85% (of approved loans, % that don't default)
- **Recall**: 70-80% (of defaulters, % identified)
- **Default detection**: Year 1 default rate <2%

---

## 5. Behavioral Analytics Model

### Model Type: Time Series + Sequence Analysis

### Approach: Hidden Markov Model + LSTM Neural Networks

### States
```python
customer_states = [
    'ACTIVE',           # Frequent interactions
    'ENGAGED',          # Regular but moderate
    'DECLINING',        # Reducing activity
    'DORMANT',          # Minimal activity
    'RE_ENGAGING'       # Recently increased activity
]

state_transitions = {
    'ACTIVE': {'ACTIVE': 0.7, 'ENGAGED': 0.2, 'DECLINING': 0.1},
    'ENGAGED': {'ENGAGED': 0.5, 'ACTIVE': 0.2, 'DECLINING': 0.3},
    'DECLINING': {'DORMANT': 0.4, 'DECLINING': 0.4, 'ENGAGED': 0.2},
    'DORMANT': {'DORMANT': 0.6, 'RE_ENGAGING': 0.2, 'ACTIVE': 0.2},
    'RE_ENGAGING': {'ACTIVE': 0.3, 'ENGAGED': 0.4, 'RE_ENGAGING': 0.3}
}
```

### Predictions
- **Next Product Interest**: What product will align with this customer?
- **Optimal Contact Timing**: When to send recommendations?
- **Service Need Prediction**: When will customer need support?
- **Life Stage**: Detect major life events affecting financial needs

### Implementation with LSTM
```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Sequence modeling
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(sequence_length, n_features)),
    Dropout(0.2),
    LSTM(32, return_sequences=False),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(output_dim, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train_sequences, y_train_sequences, epochs=50, validation_split=0.2)
```

---

## Model Training & Deployment

### Training Schedule
- **Customer Segmentation**: Monthly (less drift-sensitive)
- **Recommendation Engine**: Weekly (customer preferences evolve)
- **Churn Prediction**: Weekly (early detection critical)
- **Risk Scoring**: Every 2 weeks (regulatory requirement)
- **Behavioral**: Daily (captures latest trends)

### Model Registry & Versioning
```
models/
├── recommendation/
│   ├── v1.0/
│   │   ├── model.pkl
│   │   ├── scaler.pkl
│   │   ├── metadata.json
│   │   └── performance_metrics.json
│   ├── v1.1/
│   └── current → v1.1
├── churn/
└── risk/
```

### A/B Testing Framework
```python
# Deploy new model to 10% of users
users_group_a = sample_users(proportion=0.9)  # Old model
users_group_b = sample_users(proportion=0.1)  # New model

# Track metrics
metrics_a = track_recommendations(users_group_a, model_v1)
metrics_b = track_recommendations(users_group_b, model_v2)

# Statistical significance testing
if is_significant_improvement(metrics_a, metrics_b, alpha=0.05):
    deploy_to_production(model_v2)
```

---

## Model Monitoring & Maintenance

### Performance Drift Detection
- **Data Drift**: Input distribution changes
- **Model Drift**: Prediction performance degradation
- **Concept Drift**: Underlying relationships change

### Metrics to Monitor
- Training vs production performance gap
- Prediction confidence distribution shifts
- Feature importance changes
- Error rate increases

### Retraining Triggers
- AUC drops below 0.75
- Data drift score > 0.3
- Concept drift detected
- New data volume > trigger threshold

---

## Version: 1.0
**Last Updated**: March 2026
