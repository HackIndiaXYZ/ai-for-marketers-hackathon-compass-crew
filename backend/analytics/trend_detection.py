"""
Trend Detection Module for PainToAd AI.

Provides keyword frequency analysis, time-series preprocessing, spike and anomaly detection,
seasonal pattern identification, and trend ranking for customer feedback data.
"""

from datetime import datetime, timedelta
import logging
import re
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrendItem(BaseModel):
    """Pydantic model representing a single detected trend."""
    keyword: str
    total_occurrences: int
    trend_score: float = Field(..., description="Overall trend growth score")
    is_spike: bool = Field(..., description="True if a recent statistical spike is detected")
    seasonality_detected: bool = Field(..., description="True if periodic seasonal pattern exists")
    growth_rate_pct: float = Field(..., description="Percentage growth in recent window vs historic window")
    direction: str = Field(..., description="Rising, Falling, or Stable")
    monthly_breakdown: Dict[str, int]


class TrendReport(BaseModel):
    """Pydantic container for full trend analysis summary."""
    time_window_days: int
    total_documents_analyzed: int
    top_trends: List[TrendItem]
    spiking_keywords: List[str]
    emerging_keywords: List[str]


class TrendDetector:
    """
    Trend Detector analyzing text feedback over time to isolate keyword frequencies,
    spikes (z-scores), seasonal variations, and ranking scores.
    """

    STOPWORDS = set([
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with",
        "about", "against", "between", "into", "through", "during", "before", "after",
        "above", "below", "from", "up", "down", "of", "off", "over", "under", "again",
        "further", "then", "once", "is", "was", "are", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "doing", "i", "you", "he", "she",
        "it", "we", "they", "my", "your", "his", "her", "its", "our", "their", "this",
        "that", "these", "those", "am", "will", "can", "should", "would", "could"
    ])

    def __init__(self, spike_z_threshold: float = 2.0, min_keyword_len: int = 3) -> None:
        """
        Initialize TrendDetector.

        Args:
            spike_z_threshold: Z-score cutoff to flag a keyword surge as a spike.
            min_keyword_len: Minimum word character length to analyze.
        """
        self.spike_z_threshold = spike_z_threshold
        self.min_keyword_len = min_keyword_len
        logger.info(f"TrendDetector initialized (Z-threshold: {self.spike_z_threshold})")

    def preprocess_time_series(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Clean and preprocess customer feedback records into a structured DataFrame.

        Args:
            data: List of dicts containing 'text' and 'timestamp' (ISO string or datetime).

        Returns:
            Preprocessed Pandas DataFrame.
        """
        if not data:
            logger.warning("Empty data list passed to preprocess_time_series.")
            return pd.DataFrame(columns=["text", "timestamp", "date"])

        df = pd.DataFrame(data)
        if "text" not in df.columns or "timestamp" not in df.columns:
            raise ValueError("Input data must contain 'text' and 'timestamp' fields.")

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date
        df["text"] = df["text"].astype(str).str.lower()
        return df.sort_values("timestamp")

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract normalized n-grams/words from text excluding stop words.

        Args:
            text: Raw input string.

        Returns:
            List of valid word tokens.
        """
        words = re.findall(r'\b[a-z]{' + str(self.min_keyword_len) + r',}\b', text.lower())
        return [w for w in words if w not in self.STOPWORDS]

    def detect_spikes(self, counts_series: pd.Series) -> Tuple[bool, float]:
        """
        Perform Z-score spike detection on a time-series keyword occurrence series.

        Args:
            counts_series: Pandas Series indexed by date/time containing daily counts.

        Returns:
            Tuple of (is_spike boolean, latest z_score float)
        """
        if len(counts_series) < 3:
            return False, 0.0

        mean = counts_series.mean()
        std = counts_series.std()
        if std == 0 or np.isnan(std):
            return False, 0.0

        latest_val = counts_series.iloc[-1]
        z_score = (latest_val - mean) / std
        return z_score >= self.spike_z_threshold, round(float(z_score), 2)

    def detect_seasonality(self, counts_series: pd.Series) -> bool:
        """
        Check for 7-day or 30-day autocorrelation seasonality signals.

        Args:
            counts_series: Time series daily frequency.

        Returns:
            True if periodic autocorrelation exceeds threshold.
        """
        if len(counts_series) < 14:
            return False

        try:
            # Check 7-day lag correlation
            autocorr_7 = counts_series.autocorr(lag=7)
            return not np.isnan(autocorr_7) and autocorr_7 > 0.45
        except Exception as e:
            logger.debug(f"Seasonality calculation failed: {e}")
            return False

    def rank_trends(self, df: pd.DataFrame, top_n: int = 10) -> List[TrendItem]:
        """
        Discover, score, and rank trending keywords across the dataset.

        Args:
            df: Preprocessed DataFrame from preprocess_time_series.
            top_n: Top N trends to return.

        Returns:
            List of TrendItem Pydantic models.
        """
        if df.empty:
            return []

        # Build word occurrence matrix over dates
        word_records: List[Dict[str, Any]] = []
        for idx, row in df.iterrows():
            kws = set(self.extract_keywords(row["text"]))
            for kw in kws:
                word_records.append({"date": row["date"], "keyword": kw})

        if not word_records:
            return []

        kw_df = pd.DataFrame(word_records)
        pivot = kw_df.groupby(["date", "keyword"]).size().unstack(fill_value=0)

        # Full date range index fill
        all_dates = pd.date_range(start=df["date"].min(), end=df["date"].max())
        pivot.index = pd.to_datetime(pivot.index)
        pivot = pivot.reindex(all_dates, fill_value=0)

        results: List[TrendItem] = []
        total_days = len(all_dates)
        split_point = max(1, total_days // 2)

        for kw in pivot.columns:
            counts = pivot[kw]
            total_occurrences = int(counts.sum())
            if total_occurrences < 2:
                continue

            recent_counts = counts.iloc[split_point:]
            historic_counts = counts.iloc[:split_point]

            recent_sum = recent_counts.sum()
            historic_sum = historic_counts.sum()

            growth_rate = ((recent_sum - historic_sum) / max(historic_sum, 1)) * 100.0
            is_spike, z_score = self.detect_spikes(counts)
            is_seasonal = self.detect_seasonality(counts)

            # Trend score metric formula
            trend_score = round(total_occurrences * 0.4 + growth_rate * 0.4 + (z_score * 5.0 if is_spike else 0), 2)

            direction = "Rising" if growth_rate > 15.0 else ("Falling" if growth_rate < -15.0 else "Stable")

            # Monthly breakdown string dictionary
            monthly = counts.groupby(counts.index.strftime('%Y-%m')).sum().to_dict()
            monthly_str = {str(k): int(v) for k, v in monthly.items()}

            results.append(TrendItem(
                keyword=kw,
                total_occurrences=total_occurrences,
                trend_score=trend_score,
                is_spike=is_spike,
                seasonality_detected=is_seasonal,
                growth_rate_pct=round(growth_rate, 2),
                direction=direction,
                monthly_breakdown=monthly_str
            ))

        results.sort(key=lambda x: x.trend_score, reverse=True)
        return results[:top_n]

    def generate_report(self, data: List[Dict[str, Any]], top_n: int = 10) -> TrendReport:
        """
        Generate complete trend analysis report.

        Args:
            data: Raw text/timestamp records.
            top_n: Number of trends to extract.

        Returns:
            TrendReport object.
        """
        df = self.preprocess_time_series(data)
        top_trends = self.rank_trends(df, top_n=top_n)

        spiking = [t.keyword for t in top_trends if t.is_spike]
        emerging = [t.keyword for t in top_trends if t.direction == "Rising" and not t.is_spike]

        time_window = (df["timestamp"].max() - df["timestamp"].min()).days if not df.empty else 0

        return TrendReport(
            time_window_days=max(time_window, 1),
            total_documents_analyzed=len(df),
            top_trends=top_trends,
            spiking_keywords=spiking,
            emerging_keywords=emerging
        )


if __name__ == "__main__":
    detector = TrendDetector()
    now = datetime.now()
    sample_data = [
        {"text": "App slow latency timeout error", "timestamp": (now - timedelta(days=10)).isoformat()},
        {"text": "Huge latency timeout error in latency", "timestamp": (now - timedelta(days=2)).isoformat()},
        {"text": "Critical latency timeout crash", "timestamp": (now - timedelta(days=1)).isoformat()},
        {"text": "Latency crash error immediately", "timestamp": now.isoformat()},
    ]
    report = detector.generate_report(sample_data)
    print(report.model_dump_json(indent=2))
