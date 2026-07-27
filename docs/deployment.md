# PainToAd AI - Production Deployment & Operations Guide

## 1. Overview & Deployment Topology

PainToAd AI is deployed across high-availability cloud platforms:
- **Frontend App**: Deployed on **Vercel Edge Network** (Next.js 15 App Router).
- **Backend API**: Containerized via **Docker** and hosted on **Render Cloud Web Service**.
- **Database**: **MongoDB Atlas Cluster** (Multi-Region Cloud Replica Set).

---

## 2. Render Deployment (Backend FastAPI)

### Step 1: Prepare Repository & Environment
1. Ensure `deployment/Dockerfile.backend` exists in the repository root.
2. Push your latest code changes to GitHub.

### Step 2: Create Web Service on Render
1. Log into your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub Repository `ai-for-marketers-hackathon-compass-crew`.
4. Select Environment: **Docker**.
5. Set Dockerfile Path: `deployment/Dockerfile.backend`.
6. Select Region: Oregon (US-West) or Frankfurt (EU-Central).
7. Select Instance Type: **Standard** (or Free Tier for Hackathon demo).

### Step 3: Configure Render Environment Variables
In the Render Service settings, add the following key-value pairs:

| Variable Name | Sample / Value | Description |
| :--- | :--- | :--- |
| `ENVIRONMENT` | `production` | Production environment flag |
| `MONGODB_URL` | `mongodb+srv://user:pass@cluster.mongodb.net/...` | MongoDB Atlas URI |
| `DATABASE_NAME` | `pain_to_ad_ai_db` | Database Name |
| `GEMINI_API_KEY` | `AIzaSy...` | Google Gemini API Key |
| `SECRET_KEY` | `your-production-secret-key-32-chars` | JWT Secret Key |
| `BACKEND_CORS_ORIGINS` | `https://pain-to-ad-ai.vercel.app` | Allowed CORS Domain |

---

## 3. Vercel Deployment (Frontend Next.js 15)

### Step 1: Connect Vercel Project
1. Log into [Vercel Dashboard](https://vercel.com).
2. Click **Add New** -> **Project**.
3. Import GitHub Repository `ai-for-marketers-hackathon-compass-crew`.
4. Framework Preset: **Next.js**.
5. Root Directory: `frontend`.

### Step 2: Configure Environment Variables
In Vercel Project Settings -> **Environment Variables**:

| Variable Name | Value | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_BASE_URL` | `https://pain-to-ad-ai.onrender.com/api/v1` | Production Backend URL |
| `NEXT_PUBLIC_APP_NAME` | `PainToAd AI` | Application Name |

### Step 3: Deploy
1. Click **Deploy**. Vercel will automatically build and deploy the Next.js frontend to a global CDN.

---

## 4. Complete Environment Variables Matrix

```ini
# --- Backend Variables (.env) ---
ENVIRONMENT=production
DEBUG=False
PORT=8000
HOST=0.0.0.0
API_V1_STR=/api/v1
SECRET_KEY=pain_to_ad_ai_jwt_secret_key_prod_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
MONGODB_URL=mongodb+srv://admin:pass@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=pain_to_ad_ai_db
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
BACKEND_CORS_ORIGINS=https://pain-to-ad-ai.vercel.app,http://localhost:3000

# --- Frontend Variables (.env.local) ---
NEXT_PUBLIC_API_BASE_URL=https://pain-to-ad-ai.onrender.com/api/v1
NEXT_PUBLIC_APP_NAME=PainToAd AI
```

---

## 5. Production Readiness Checklist

- [x] **CORS Lockdown**: Backend restricted to Vercel production domain.
- [x] **Database Security**: Network IP Whitelist configured in MongoDB Atlas.
- [x] **API Secrets**: All secrets loaded exclusively through environment variables.
- [x] **Health Checks**: `/api/v1/health` endpoint returning `200 OK`.
- [x] **HTTPS Enforcement**: SSL/TLS active on Vercel and Render endpoints.
- [x] **Nginx Proxy**: Nginx container ready for custom server reverse proxy deployment.
