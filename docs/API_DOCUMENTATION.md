# REST API Documentation

## Base URL
`https://api.aiidigitalbank.com/api/v1`

## Authentication
All requests require Bearer token in Authorization header:
```
Authorization: Bearer <your-api-token>
```

---

## Customer Endpoints

### Get Customer Profile
```
GET /customers/{customer_id}

Response:
{
  "customer_id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "kyc_status": "VERIFIED",
  "risk_profile": "MODERATE",
  "total_balance": 50000.00,
  "created_at": "2026-01-15T10:30:00Z"
}
```

### Get Customer 360 Profile
```
GET /customers/{customer_id}/profile

Response:
{
  "customer_id": "uuid",
  "demographics": {...},
  "financial_snapshot": {...},
  "behavioral_profile": {...},
  "predictive_metrics": {
    "lifetime_value": 75000,
    "churn_risk": 0.15,
    "segment": "GROWING_PROFESSIONALS"
  }
}
```

---

## Product Endpoints

### List All Products
```
GET /products?limit=10&offset=0&type=BONDS

Response:
[
  {
    "product_id": "uuid",
    "name": "Corporate Bond Fund",
    "type": "BONDS",
    "min_investment": 5000,
    "expected_return": 6.5,
    "risk_level": "MEDIUM"
  }
]
```

---

## Recommendation Endpoints

### Get Recommendations for Customer
```
GET /customers/{customer_id}/recommendations?limit=5

Response:
[
  {
    "recommendation_id": "uuid",
    "product_id": "uuid",
    "product_name": "Corporate Bond Fund",
    "score": 0.85,
    "reason": "Matches your risk profile",
    "expected_return": 6.5
  }
]
```

### Generate Recommendations
```
POST /recommendations/generate

Request:
{
  "customer_id": "uuid",
  "product_limit": 5,
  "rerank_method": "diversity"
}

Response:
{
  "recommendations": [...],
  "generated_at": "2026-03-26T10:30:00Z"
}
```

---

## Analytics Endpoints

### Customer Analytics
```
GET /analytics/customer/{customer_id}

Response:
{
  "customer_id": "uuid",
  "total_transactions_30d": 25,
  "total_volume_30d": 15000,
  "engagement_score": 0.78,
  "satisfaction_score": 0.82,
  "product_adoption": ["SAVINGS", "BONDS"]
}
```

### Dashboard Analytics
```
GET /analytics/dashboard

Response:
{
  "total_customers": 1000000,
  "active_customers_30d": 750000,
  "total_aum": 500000000,
  "average_customer_value": 500000,
  "cross_sell_rate": 0.35,
  "customer_segments": {...}
}
```

---

## Risk Endpoints

### Risk Assessment
```
GET /risk/assessment/{customer_id}

Response:
{
  "customer_id": "uuid",
  "risk_score": 0.12,
  "risk_level": "B",
  "default_probability": 0.12,
  "decision": "APPROVE_WITH_CONDITIONS"
}
```

### Fraud Score
```
POST /risk/fraud-score

Request:
{
  "transaction_id": "uuid",
  "amount": 5000,
  "merchant_category": "TRAVEL",
  "location": "NEW_YORK"
}

Response:
{
  "fraud_score": 0.05,
  "risk_level": "LOW",
  "decision": "APPROVE"
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Server Error |

---

## Rate Limiting

- 1000 requests per hour per API key
- Headers in response:
  - `X-RateLimit-Limit`: 1000
  - `X-RateLimit-Remaining`: 999
  - `X-RateLimit-Reset`: timestamp

---

## Version: 1.0
**Last Updated**: March 2026
