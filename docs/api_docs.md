# PainToAd AI - OpenAPI & REST API Specification

**Base URL**: `https://pain-to-ad-ai.onrender.com/api/v1`  
**Local Development**: `http://localhost:8000/api/v1`  
**Authentication**: Bearer JWT (`Authorization: Bearer <token>`)

---

## 1. System Health & System Endpoints

### `GET /health`
Verifies backend service operational status and database connection.

- **Headers**: None required
- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "PainToAd AI Backend operational",
  "timestamp": "2026-07-27T15:00:00Z",
  "data": {
    "version": "1.0.0",
    "environment": "production",
    "database": "connected",
    "ai_engine": "online"
  }
}
```

---

## 2. Authentication Endpoints

### `POST /auth/register`
Registers a new user account.

- **Request Body**:
```json
{
  "email": "marketer@company.com",
  "password": "StrongPassword123!",
  "full_name": "Sarah Connor",
  "company_name": "Growth Hacker Inc"
}
```

- **Response `201 Created`**:
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": "usr_9a8b7c6d5e4f",
    "email": "marketer@company.com",
    "full_name": "Sarah Connor",
    "created_at": "2026-07-27T15:00:00Z"
  }
}
```

### `POST /auth/login`
Authenticates user credentials and returns JWT bearer token.

- **Request Body**:
```json
{
  "email": "marketer@company.com",
  "password": "StrongPassword123!"
}
```

- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "Authentication successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in_minutes": 10080
  }
}
```

---

## 3. Scraper & Customer Intelligence Endpoints

### `POST /intelligence/scrape`
Crawls public online discussions for customer pain points.

- **Request Body**:
```json
{
  "niche": "SaaS Customer Churn",
  "keywords": ["churn rate", "customer retention", "cancellation reason"],
  "sources": ["reddit", "twitter", "g2"],
  "max_results": 50
}
```

- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "Scraping completed successfully",
  "data": {
    "job_id": "job_3f2e1d0c9b8a",
    "total_scraped": 48,
    "top_pain_points": [
      {
        "pain_id": "pain_101",
        "category": "Customer Support Delay",
        "frustration_score": 8.7,
        "sample_quote": "It takes 3 days to get a single response from support when our billing fails.",
        "frequency": 14
      }
    ]
  }
}
```

---

## 4. Campaign Generation Endpoints

### `POST /campaigns/generate`
Triggers Gemini 1.5 Pro and LangGraph agents to generate ad campaigns.

- **Request Body**:
```json
{
  "product_name": "RetainFlow SaaS",
  "target_audience": "B2B SaaS Founders & Product Managers",
  "niche": "Customer Retention & Churn Reduction",
  "platforms": ["meta", "google", "linkedin"],
  "ad_tone": "Urgent, Solution-Oriented, High-Converting",
  "budget": 1000.00
}
```

- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "Campaign generated successfully",
  "data": {
    "campaign_id": "campaign_a1b2c3d4e5f6",
    "product_name": "RetainFlow SaaS",
    "created_at": "2026-07-27T15:05:00Z",
    "ad_variants": [
      {
        "platform": "meta",
        "headline": "Stop Losing $10k/Month to Hidden SaaS Churn",
        "primary_text": "Tired of users canceling without leaving feedback? RetainFlow isolates churn risks in real-time before you lose the account.",
        "call_to_action": "Start Free 14-Day Trial",
        "hook_angle": "Agitation of Financial Loss"
      },
      {
        "platform": "google",
        "headline": "Automated Churn Reduction Tool | Fix Retention Fast",
        "primary_text": "Turn exit surveys into instant recovery offers. Boost SaaS retention by 34% in 30 days.",
        "call_to_action": "Get Demo Now",
        "hook_angle": "Direct Benefit & ROI Proof"
      }
    ]
  }
}
```

---

## 5. Predictive ROI & Analytics Endpoints

### `POST /analytics/predict`
Computes predictive conversion rate, projected CTR, and ROI multiplier.

- **Request Body**:
```json
{
  "campaign_id": "campaign_a1b2c3d4e5f6",
  "ad_spend": 1500.00,
  "target_reach": 50000,
  "avg_customer_value": 250.00
}
```

- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "ROI analytics prediction generated",
  "data": {
    "campaign_id": "campaign_a1b2c3d4e5f6",
    "estimated_ctr": "3.45%",
    "estimated_clicks": 1725,
    "conversion_rate": "4.20%",
    "estimated_conversions": 72,
    "gross_revenue": "$18,000.00",
    "ad_spend": "$1,500.00",
    "net_profit": "$16,500.00",
    "roi_percentage": "1100.00%",
    "cost_per_acquisition": "$20.83"
  }
}
```
