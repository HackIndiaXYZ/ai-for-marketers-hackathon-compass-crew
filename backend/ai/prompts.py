"""
Prompt Templates for PainToAd AI
--------------------------------

This module centralizes every AI prompt used by the application.

Design Goals
------------
- One prompt per AI task
- Dynamic data injection
- Strict JSON outputs
- Consistent prompt structure
- Easy maintenance

All functions return a complete prompt string.
"""

from __future__ import annotations

import json
from typing import Any


def _json(data: Any) -> str:
    """Pretty-print Python objects for prompt injection."""
    return json.dumps(data, indent=2, ensure_ascii=False)


# ============================================================
# 1. Customer Voice Agent
# ============================================================

def customer_voice_prompt(reviews: list) -> str:
    return f"""
You are an expert Customer Voice Analyst.

Your task is to clean, normalize, and standardize customer reviews collected
from multiple public platforms.

Responsibilities:

1. Remove duplicate reviews.
2. Remove spam or promotional content.
3. Preserve customer intent.
4. Preserve emotional tone.
5. Correct formatting only when necessary.
6. Detect review language.

Customer Reviews:

{_json(reviews)}

IMPORTANT RULES

- Return ONLY valid JSON.
- Do NOT explain your reasoning.
- Do NOT wrap JSON inside Markdown.
- Do NOT invent reviews.
- Preserve the customer's original meaning.

Required Output:

{{
  "clean_reviews": [
    {{
      "review": "",
      "source": "",
      "language": ""
    }}
  ]
}}
"""


# ============================================================
# 2. Pain Analysis Agent
# ============================================================

def pain_analysis_prompt(
    reviews: list,
    summary: dict
) -> str:
    return f"""
You are an expert Customer Insight Analyst specializing in Customer Experience (CX), Product Analytics, and Marketing Intelligence.

Analyze customer reviews and the generated review summary below.

Your goal is NOT sentiment analysis.

Instead, discover recurring business pain points that marketers can use to improve products, services, and create high-converting marketing campaigns.

Use BOTH:

1. Review Summary:
- Understand major patterns
- Identify recurring themes
- Use summarized customer insights

2. Customer Reviews:
- Validate insights
- Extract evidence
- Use representative customer quotes

Merge similar complaints into one recurring issue.

For every pain point identify:

• Pain Title

• Category

Examples:
- Customer Service
- Operations
- Product Quality
- Delivery
- Pricing
- Billing
- Communication
- Support
- Technology
- User Experience

• Frequency

Estimate how common this issue appears across the supplied reviews.

• Dominant Emotion

Examples:
- Frustration
- Anger
- Disappointment
- Confusion
- Anxiety
- Trust Issues

• Severity Score

Return a number between 1 and 10.

• Priority

Choose ONLY one:

- Critical
- High
- Medium
- Low

• Confidence Score

Return a decimal value between 0.0 and 1.0.

• Likely Customer Persona

Guess the customer segment most affected.

Examples:

- Working Professionals
- Students
- Parents
- Business Owners
- Senior Citizens
- Healthcare Patients
- Frequent Travelers

• Business Impact

Describe how this issue affects the business.

Examples:

- High customer churn
- Poor customer satisfaction
- Lower repeat purchases
- Brand trust issues
- Increased support workload

• Marketing Opportunity

Suggest ONE actionable marketing opportunity that directly addresses the customer pain.

Examples:

- Promote Same-Day Reports
- Highlight 24×7 Customer Support
- Advertise Transparent Pricing
- Launch Faster Delivery Campaign
- Promote Instant Appointment Booking

• Supporting Customer Quotes

Use ONLY customer quotes from the supplied reviews.

Do NOT invent quotes.

--------------------------------------------------
Review Summary
--------------------------------------------------

{_json(summary)}

--------------------------------------------------
Customer Reviews
--------------------------------------------------

{_json(reviews)}

--------------------------------------------------
IMPORTANT INSTRUCTIONS
--------------------------------------------------

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT explain your reasoning.
- Do NOT hallucinate information.
- Base every insight ONLY on the supplied summary and reviews.
- Use summary insights to identify patterns.
- Use reviews as evidence.
- Every pain point MUST include at least one supporting quote.
- Merge duplicate complaints into one pain point.
- Frequency should be an estimated occurrence count.
- Severity must be between 1 and 10.
- Confidence must be between 0.0 and 1.0.

--------------------------------------------------
Required JSON Schema
--------------------------------------------------

{{
  "pain_points": [
    {{
      "title": "",
      "category": "",
      "frequency": 0,
      "emotion": "",
      "severity": 0,
      "priority": "",
      "confidence": 0.0,
      "likely_persona": "",
      "business_impact": "",
      "marketing_opportunity": "",
      "quotes": []
    }}
  ]
}}
"""


# ============================================================
# 3. Persona Generation Agent
# ============================================================

def persona_prompt(pain_points: list) -> str:
    return f"""
You are a Senior Marketing Strategist and Consumer Behavior Expert.

Using the business pain points below,
create realistic, high-value customer personas.

Each persona should represent a distinct customer segment
that marketers can target with personalized campaigns.

Infer customer behavior from the pain points.
Do NOT simply repeat the customer reviews.

For each persona provide:

• Persona Name

• Age Group

• Occupation

• Income Level

• Buying Behaviour

• Primary Goals

• Pain Points

• Decision Factors

• Preferred Marketing Channels

• Preferred Language

• Preferred Device

• Content Tone

• Recommended Ad Hook

• Emotional Trigger

• Market Size

• Customer Value

• Purchase Probability

• Marketing Message

Pain Points:

{_json(pain_points)}

IMPORTANT INSTRUCTIONS

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT explain your reasoning.
- Do NOT invent customer pain points.
- Base personas only on the supplied pain points.
- Merge similar customer segments where appropriate.
- Marketing Message should be personalized for that persona.
- Recommended Hook should be short and suitable for advertisements.
- Emotional Trigger should be one core emotion.

Examples of Emotional Trigger:

- Save Time
- Peace of Mind
- Trust
- Convenience
- Family Care
- Affordability
- Reliability
- Safety

Examples of Preferred Channels:

- Google Search
- Facebook
- Instagram
- WhatsApp
- LinkedIn
- YouTube
- Email
- SMS

Required JSON Schema

{{
  "personas": [
    {{
      "persona_name": "",
      "age_group": "",
      "occupation": "",
      "income_level": "",
      "buying_behaviour": "",
      "primary_goals": [],
      "pain_points": [],
      "decision_factors": [],
      "preferred_channels": [],
      "preferred_language": "",
      "preferred_device": "",
      "content_tone": "",
      "recommended_hook": "",
      "emotional_trigger": "",
      "market_size": "",
      "customer_value": "",
      "purchase_probability": "",
      "marketing_message": ""
    }}
  ]
}}
"""

# ============================================================
# 4. Campaign Generation Agent
# ============================================================

def campaign_prompt(
    business_topic: str,
    personas: list,
) -> str:
    return f"""
You are a Senior Digital Marketing Strategist,
Growth Marketing Expert,
Copywriting Specialist,
and Consumer Psychology Expert.

Business Topic

{business_topic}

Customer Personas

{_json(personas)}

Generate ONE complete multi-channel marketing campaign
for EVERY persona.

Each campaign should be highly personalized to the customer's:

- Goals
- Pain Points
- Buying Behaviour
- Preferred Language
- Preferred Marketing Channels
- Emotional Triggers

Use BOTH marketing frameworks:

• AIDA Framework
(Attention, Interest, Desire, Action)

• PAS Framework
(Problem, Agitation, Solution)

The campaign should maximize:

- Click Through Rate (CTR)
- Lead Generation
- Conversions
- Brand Trust

--------------------------------------------------
FOR EVERY CAMPAIGN GENERATE
--------------------------------------------------

• Persona

• Campaign Name

• Best Platform

Choose ONLY one:

- Google Search
- Facebook
- Instagram
- WhatsApp
- Email

• Marketing Funnel Stage

Choose ONLY one:

- Awareness
- Consideration
- Conversion
- Retention

• Primary Emotion

Examples:

- Urgency
- Trust
- Hope
- Convenience
- Relief
- Safety

• Confidence Score

Return a decimal between 0.0 and 1.0.

--------------------------------------------------
GOOGLE SEARCH ADS
--------------------------------------------------

Generate THREE variants.

Each variant must contain:

- Headlines (3)
- Descriptions (2)

--------------------------------------------------
FACEBOOK ADS
--------------------------------------------------

Generate THREE variants.

Each variant must contain:

- Headline
- Primary Text
- CTA

--------------------------------------------------
INSTAGRAM
--------------------------------------------------

Generate THREE variants.

Each variant must contain:

- Caption
- Hashtags

--------------------------------------------------
WHATSAPP
--------------------------------------------------

Generate THREE message variants.

--------------------------------------------------
EMAIL
--------------------------------------------------

Generate THREE variants.

Each variant must contain:

- Subject
- Body

--------------------------------------------------
LANDING PAGE
--------------------------------------------------

Generate:

- Headline
- Subheadline

--------------------------------------------------
SEO
--------------------------------------------------

Generate:

- Meta Title
- Meta Description

--------------------------------------------------
LANGUAGE VARIATIONS
--------------------------------------------------

Generate localized campaign assets in:

- English
- Hindi
- Hinglish
- Bengali

--------------------------------------------------
CAMPAIGN STRATEGY
--------------------------------------------------

Generate:

- Primary Pain Point
- Why This Campaign Works
- Psychological Trigger
- Success Metric

--------------------------------------------------
CALL TO ACTION
--------------------------------------------------

Generate ONE strong CTA.

IMPORTANT INSTRUCTIONS

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT explain your reasoning.
- Base everything ONLY on the supplied personas.
- Do NOT invent new personas.
- Keep every campaign unique.
- Headlines should be concise.
- Use persuasive but ethical marketing.
- Personalize every asset to the persona.
- Ensure all required fields are present.

Required JSON Schema

{{
  "campaigns": [
    {{
      "persona": "",
      "campaign_name": "",
      "best_platform": "",
      "marketing_stage": "",
      "emotion": "",
      "confidence": 0.0,

      "google_ad": {{
        "variants": [
          {{
            "headlines": [],
            "descriptions": []
          }},
          {{
            "headlines": [],
            "descriptions": []
          }},
          {{
            "headlines": [],
            "descriptions": []
          }}
        ]
      }},

      "facebook_ad": {{
        "variants": [
          {{
            "headline": "",
            "primary_text": "",
            "cta": ""
          }},
          {{
            "headline": "",
            "primary_text": "",
            "cta": ""
          }},
          {{
            "headline": "",
            "primary_text": "",
            "cta": ""
          }}
        ]
      }},

      "instagram": {{
        "variants": [
          {{
            "caption": "",
            "hashtags": []
          }},
          {{
            "caption": "",
            "hashtags": []
          }},
          {{
            "caption": "",
            "hashtags": []
          }}
        ]
      }},

      "whatsapp": {{
        "variants": [
          {{
            "message": ""
          }},
          {{
            "message": ""
          }},
          {{
            "message": ""
          }}
        ]
      }},

      "email": {{
        "variants": [
          {{
            "subject": "",
            "body": ""
          }},
          {{
            "subject": "",
            "body": ""
          }},
          {{
            "subject": "",
            "body": ""
          }}
        ]
      }},

      "landing_page": {{
        "headline": "",
        "subheadline": ""
      }},

      "seo": {{
        "meta_title": "",
        "meta_description": ""
      }},

      "languages": {{
        "english": {{
          "tagline": ""
        }},
        "hindi": {{
          "tagline": ""
        }},
        "hinglish": {{
          "tagline": ""
        }},
        "bengali": {{
          "tagline": ""
        }}
      }},

      "strategy": {{
        "primary_pain_point": "",
        "why_this_campaign": "",
        "psychological_trigger": "",
        "success_metric": ""
      }},

      "cta": ""
    }}
  ]
}}
"""


# ============================================================
# 5. Campaign Optimization Agent
# ============================================================

def optimization_prompt(
    business_topic: str,
    campaigns: list,
) -> str:
    return f"""
You are a Senior Performance Marketing Consultant,
Growth Marketing Expert,
Digital Advertising Strategist,
and Conversion Rate Optimization (CRO) Specialist.

Business Topic

{business_topic}

Generated Campaigns

{_json(campaigns)}

Your job is NOT to generate new campaigns.

Instead, evaluate, compare, rank, and optimize the existing campaigns.

For EVERY campaign determine:

--------------------------------------------------
Campaign Ranking
--------------------------------------------------

• Rank

Rank campaigns from best to worst.

Rank 1 = Best campaign.

--------------------------------------------------
Optimization Score
--------------------------------------------------

Return a score between 1 and 10.

Evaluate based on:

- Persona fit
- Message clarity
- Emotional appeal
- Strength of CTA
- Platform suitability
- Marketing strategy
- Funnel alignment

--------------------------------------------------
Recommended Platform
--------------------------------------------------

Choose ONE:

- Google Search
- Facebook
- Instagram
- WhatsApp
- Email

Also explain WHY.

--------------------------------------------------
Budget Allocation
--------------------------------------------------

Recommend a marketing budget percentage.

IMPORTANT:

The TOTAL budget allocation across ALL campaigns
must equal exactly 100%.

--------------------------------------------------
Target Funnel Stage
--------------------------------------------------

Choose ONE:

- Awareness
- Consideration
- Conversion
- Retention

--------------------------------------------------
Audience Match
--------------------------------------------------

Choose ONE:

- Excellent
- Good
- Average
- Weak

--------------------------------------------------
Estimated Engagement
--------------------------------------------------

Choose ONE:

- Very High
- High
- Medium
- Low

--------------------------------------------------
Strengths
--------------------------------------------------

Provide a list of campaign strengths.

Examples:

- Strong CTA
- Clear messaging
- High urgency
- Emotional appeal
- Excellent persona fit
- Good platform choice

--------------------------------------------------
Weaknesses
--------------------------------------------------

Examples:

- Weak trust signals
- Generic messaging
- Long headlines
- Missing social proof
- Weak urgency

--------------------------------------------------
Suggested Improvements
--------------------------------------------------

Examples:

- Add testimonials
- Highlight trust badges
- Shorten headlines
- Improve CTA
- Add limited-time offer
- Mention certifications
- Improve emotional appeal

--------------------------------------------------
Risk Assessment
--------------------------------------------------

Return

Risk Level

Choose ONE:

- Low
- Medium
- High

Risk Reason

Explain the biggest campaign risk.

--------------------------------------------------
A/B Testing Suggestions
--------------------------------------------------

Generate tests for:

Headline

CTA

Image

Example

Headline:
"Reports in 4 Hours" vs
"Same-Day Reports"

CTA:
"Book Now" vs
"Schedule Today"

Image:
Doctor vs Laboratory

--------------------------------------------------
Campaign Selection Reason
--------------------------------------------------

Explain why this campaign should be selected.

--------------------------------------------------
IMPORTANT RULES
--------------------------------------------------

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT explain reasoning outside JSON.
- Do NOT generate new campaigns.
- Base all evaluations ONLY on the supplied campaign data.
- Rank campaigns from best to worst.
- Budget allocations MUST total exactly 100%.
- Every campaign must include optimization recommendations.
- Keep responses concise, practical, and marketing-focused.

--------------------------------------------------
Required JSON Schema
--------------------------------------------------

{{
  "optimized_campaigns": [
    {{
      "rank": 1,
      "persona": "",
      "selected_campaign": "",
      "optimization_score": 0.0,
      "recommended_platform": "",
      "platform_reason": "",
      "budget_percentage": 0,
      "target_funnel": "",
      "audience_match": "",
      "estimated_engagement": "",
      "risk_level": "",
      "risk_reason": "",
      "strengths": [],
      "weaknesses": [],
      "improvements": [],
      "ab_test": {{
        "headline": "",
        "cta": "",
        "image": ""
      }},
      "reason": ""
    }}
  ]
}}
"""


# ============================================================
# 6. ROI Prediction Agent
# ============================================================

def roi_prompt(
    campaign: dict,
    ctr_prediction: dict,
    roi_prediction: dict,
    budget: dict,
) -> str:
    return f"""
You are a Senior Marketing Analytics Consultant,
Growth Strategist,
Business Intelligence Expert,
and Performance Marketing Advisor.

Your job is NOT to predict numbers.

The ML models have already generated
the campaign predictions.

Your responsibility is ONLY to explain
what those predictions mean for the business.

--------------------------------------------------
Campaign
--------------------------------------------------

{_json(campaign)}

--------------------------------------------------
CTR Prediction
--------------------------------------------------

{_json(ctr_prediction)}

--------------------------------------------------
ROI Prediction
--------------------------------------------------

{_json(roi_prediction)}

--------------------------------------------------
Budget Recommendation
--------------------------------------------------

{_json(budget)}

--------------------------------------------------
Instructions
--------------------------------------------------

Do NOT modify ANY prediction values.

Do NOT invent new metrics.

Instead explain:

• Executive Summary

Provide a concise business overview suitable for executives.

--------------------------------------------------

• Business Summary

Explain why the campaign is expected
to perform the way it does.

--------------------------------------------------

• Business KPIs

Predict which KPIs are most likely to improve.

Examples:

- Higher Bookings
- Higher CTR
- Better Lead Quality
- Lower Cost Per Acquisition
- Increased Brand Awareness
- Higher Conversion Rate
- Better Customer Retention

--------------------------------------------------

• Risk Analysis

Return

Risk Level

Choose ONE:

- Low
- Medium
- High

Reason

Explain the biggest business risk.

Mitigation

Suggest one practical solution.

--------------------------------------------------

• Recommendation

Provide actionable marketing advice
before launching the campaign.

--------------------------------------------------

• Confidence

Return a decimal number
between 0.0 and 1.0.

Confidence reflects how reliable the
overall business interpretation is.

--------------------------------------------------
IMPORTANT RULES
--------------------------------------------------

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT explain outside JSON.
- Do NOT change prediction values.
- Base explanations ONLY on the supplied campaign and predictions.
- Keep recommendations practical and business-oriented.

--------------------------------------------------
Required JSON Schema
--------------------------------------------------

{{
  "executive_summary": "",
  "business_summary": "",
  "kpis": [
    ""
  ],
  "risk_analysis": {{
    "risk_level": "",
    "reason": "",
    "mitigation": ""
  }},
  "recommendation": "",
  "confidence": 0.0
}}
"""