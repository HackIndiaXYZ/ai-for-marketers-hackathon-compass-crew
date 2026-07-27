# PainToAd AI - System Workflow & Execution Lifecycles

## 1. Complete User Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Marketer / User
    participant Frontend as Next.js 15 App
    participant Backend as FastAPI Backend
    participant Agents as LangGraph Multi-Agent Engine
    participant Gemini as Google Gemini 1.5 Pro API
    participant Database as MongoDB Atlas

    User->>Frontend: 1. Inputs Target Niche / Product URL / Keywords
    Frontend->>Backend: 2. POST /api/v1/intelligence/analyze
    Backend->>Agents: 3. Trigger ScraperAgent & Data Collection
    Agents-->>Backend: 4. Scraped Comments & Discussions
    Backend->>Agents: 5. Trigger AnalysisAgent (Vector Embedding + Clustering)
    Agents->>Database: 6. Store Structured Pain Points & Embeddings
    Backend->>Agents: 7. Trigger CopywriterAgent with Pain Matrix
    Agents->>Gemini: 8. Prompt Gemini 1.5 Pro for Ad Copy Variants
    Gemini-->>Agents: 9. Returns Tailored Ad Creatives & Hooks
    Backend->>Agents: 10. Trigger PredictionAgent for ROI & CTR Modeling
    Agents-->>Backend: 11. Consolidated Campaign Package
    Backend->>Database: 12. Save Campaign & Analytics Record
    Backend-->>Frontend: 13. Returns JSON Payload (Campaign + Analytics)
    Frontend-->>User: 14. Displays Interactive Campaign Dashboard & Export Options
```

---

## 2. Detailed User Flow Description

1. **Campaign Initialization**:
   - The user navigates to the PainToAd AI Dashboard.
   - User submits product details, target audience criteria (e.g., "SaaS founders frustrated with churn"), and target platform preferences (Meta, Google, LinkedIn).
2. **Data Collection & Crawling**:
   - PainToAd AI automatically scans public discussions across Reddit subreddits, X threads, G2 reviews, and community forums for target keywords.
3. **Pain Point Intelligence**:
   - Raw data is filtered, sanitized, and clustered into actionable pain point vectors.
   - Emotional intensity, frustration scores, and urgency markers are computed.
4. **AI Campaign Generation**:
   - LangGraph orchestrates the generation of multi-platform ad variations:
     - **Headline**: High-converting hook addressing the exact pain point phrasing.
     - **Primary Text**: Problem-Agitate-Solution (PAS) or Attention-Interest-Desire-Action (AIDA) frameworks.
     - **Call to Action**: High-intent conversion trigger.
5. **Predictive Performance Analytics**:
   - Simulated CTR, projected conversion rate, estimated CPC, and ROI multiplier are calculated based on benchmark metrics.
6. **Campaign Export & Deployment**:
   - Marketers can review, edit, copy, or export ad campaigns in CSV/JSON formats or push directly to ad channels.

---

## 3. End-to-End System & Request Lifecycle

```mermaid
graph TD
    A[Client Request] --> B{Valid Authentication?}
    B -- No --> C[401 Unauthorized Response]
    B -- Yes --> D[FastAPI Route Handler]
    D --> E[Validate Pydantic Input Schema]
    E --> F[Check MongoDB Cache / Existing Analysis]
    F -- Cache Hit --> G[Return Cached Analytics JSON]
    F -- Cache Miss --> H[Dispatch LangGraph Workflow]
    H --> I[Execute Scraper Task]
    I --> J[Generate Text Embeddings via SentenceTransformers]
    J --> K[Query Gemini 1.5 Pro via Async Client]
    K --> L[Format Ad Copy & Run ROI Math]
    L --> M[Write to MongoDB Atlas Collections]
    M --> N[Return 200 OK Response]
```

---

## 4. LangGraph Multi-Agent Flow State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> DataScrapingState: User Trigger
    DataScrapingState --> TextSanitizationState: Raw Data Fetched
    TextSanitizationState --> VectorEmbeddingState: Clean Text Prepared
    VectorEmbeddingState --> ClusteringState: Embeddings Generated
    ClusteringState --> CopywritingState: Pain Clusters Identified
    CopywritingState --> PerformancePredictionState: Ad Variations Formatted
    PerformancePredictionState --> PersistenceState: ROI Metrics Calculated
    PersistenceState --> [*]: Response Delivered
```
