"""
PainToAd AI - General Helpers & Utility Functions
=================================================
Contains robust utility methods for response formatting, string sanitization,
campaign ROI prediction metrics, and data processing.
"""

import re
import uuid
import html
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone


def format_response(
    status: str = "success",
    message: str = "Operation completed successfully",
    data: Optional[Any] = None,
    meta: Optional[Dict[str, Any]] = None,
    error_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Standardized API response wrapper for consistent REST API responses across frontend and backend.
    """
    response = {
        "status": status,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data if data is not None else {},
    }
    if meta:
        response["meta"] = meta
    if error_code:
        response["error_code"] = error_code
    return response


def sanitize_text(raw_text: str) -> str:
    """
    Sanitizes raw scraped customer feedback text by stripping HTML, removing extra whitespace,
    and normalizing unprintable characters.
    """
    if not raw_text:
        return ""

    # Unescape HTML entities
    text = html.unescape(raw_text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def generate_unique_id(prefix: str = "campaign") -> str:
    """
    Generates a unique prefixed identifier using UUIDv4.
    """
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def calculate_roi_metrics(
    target_audience_size: int,
    estimated_ctr: float,
    conversion_rate: float,
    avg_customer_value: float,
    ad_spend: float
) -> Dict[str, float]:
    """
    Calculates estimated marketing campaign ROI, impressions, clicks, conversions, and revenue.

    Parameters:
        target_audience_size (int): Estimated total reach
        estimated_ctr (float): Click-Through-Rate percentage (e.g., 2.5 for 2.5%)
        conversion_rate (float): Conversion rate percentage (e.g., 3.0 for 3.0%)
        avg_customer_value (float): Average Revenue Per Paying Customer ($)
        ad_spend (float): Total advertising budget allocation ($)

    Returns:
        Dict containing projected Clicks, Conversions, Gross Revenue, Net Profit, and ROI %.
    """
    clicks = round((target_audience_size * (estimated_ctr / 100.0)), 0)
    conversions = round((clicks * (conversion_rate / 100.0)), 0)
    gross_revenue = round(conversions * avg_customer_value, 2)
    net_profit = round(gross_revenue - ad_spend, 2)

    roi_percentage = 0.0
    if ad_spend > 0:
        roi_percentage = round((net_profit / ad_spend) * 100.0, 2)

    return {
        "estimated_clicks": clicks,
        "estimated_conversions": conversions,
        "gross_revenue": gross_revenue,
        "net_profit": net_profit,
        "roi_percentage": roi_percentage,
        "cost_per_acquisition": round(ad_spend / max(conversions, 1), 2)
    }


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    Extracts high-frequency keywords from customer pain point text.
    """
    clean_str = re.sub(r'[^\w\s]', '', text.lower())
    words = clean_str.split()

    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "about",
        "against", "between", "into", "through", "during", "before", "after", "above", "below", "from",
        "up", "down", "in", "out", "off", "over", "under", "again", "further", "then", "once", "here",
        "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most",
        "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
        "s", "t", "can", "will", "just", "don", "should", "now", "i", "my", "we", "our", "you", "your",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "this", "that"
    }

    filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    frequency: Dict[str, int] = {}
    for word in filtered_words:
        frequency[word] = frequency.get(word, 0) + 1

    sorted_words = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    return [word for word, count in sorted_words[:top_n]]
