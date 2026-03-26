"""
Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI in Digital Banking",
    description="Intelligent Digital Banking Platform with AI/ML",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# ==================== Root Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI in Digital Banking API",
        "version": "1.0.0",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


# ==================== Customer Endpoints ====================

@app.get("/api/v1/customers/{customer_id}")
async def get_customer(customer_id: str):
    """Get customer profile"""
    return {
        "customer_id": customer_id,
        "name": "John Doe",
        "email": "john@example.com",
        "kyc_status": "VERIFIED",
        "total_balance": 50000.00,
        "created_at": "2026-01-15T10:30:00Z"
    }


@app.get("/api/v1/customers/{customer_id}/profile")
async def get_customer_360(customer_id: str):
    """Get customer 360° profile"""
    return {
        "customer_id": customer_id,
        "demographics": {
            "age": 35,
            "gender": "M",
            "location": "New York"
        },
        "financial_snapshot": {
            "total_assets": 50000,
            "monthly_revenue": 5000,
            "liabilities": 10000
        },
        "behavioral_profile": {
            "transaction_frequency": "HIGH",
            "login_frequency": "DAILY"
        },
        "predictive_metrics": {
            "lifetime_value": 75000,
            "churn_risk": 0.15,
            "segment": "GROWING_PROFESSIONALS"
        }
    }


# ==================== Product Endpoints ====================

@app.get("/api/v1/products")
async def list_products(limit: int = 10, offset: int = 0, product_type: str = None):
    """List all products"""
    return {
        "total": 50,
        "limit": limit,
        "offset": offset,
        "products": [
            {
                "product_id": "prod_123",
                "name": "Corporate Bond Fund",
                "type": "BONDS",
                "min_investment": 5000,
                "expected_return": 6.5,
                "risk_level": "MEDIUM"
            }
        ]
    }


# ==================== Recommendation Endpoints ====================

@app.get("/api/v1/customers/{customer_id}/recommendations")
async def get_recommendations(customer_id: str, limit: int = 5):
    """Get recommendations for customer"""
    return {
        "customer_id": customer_id,
        "recommendations": [
            {
                "recommendation_id": "rec_123",
                "product_id": "prod_456",
                "product_name": "Corporate Bond Fund",
                "score": 0.85,
                "reason": "Matches your risk profile",
                "expected_return": 6.5
            }
        ],
        "generated_at": datetime.utcnow().isoformat()
    }


# ==================== Analytics Endpoints ====================

@app.get("/api/v1/analytics/customer/{customer_id}")
async def get_analytics(customer_id: str):
    """Get customer analytics"""
    return {
        "customer_id": customer_id,
        "transactions_30d": 25,
        "total_volume_30d": 15000,
        "engagement_score": 0.78,
        "satisfaction_score": 0.82,
        "products": ["SAVINGS", "BONDS"]
    }


@app.get("/api/v1/analytics/dashboard")
async def get_dashboard_analytics():
    """Get dashboard analytics"""
    return {
        "total_customers": 1000000,
        "active_customers_30d": 750000,
        "total_aum": 500000000,
        "average_customer_value": 500000,
        "cross_sell_rate": 0.35
    }


# ==================== Risk Endpoints ====================

@app.get("/api/v1/risk/assessment/{customer_id}")
async def get_risk_assessment(customer_id: str):
    """Get risk assessment for customer"""
    return {
        "customer_id": customer_id,
        "risk_score": 0.12,
        "risk_level": "B",
        "default_probability": 0.12,
        "decision": "APPROVE_WITH_CONDITIONS"
    }


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
