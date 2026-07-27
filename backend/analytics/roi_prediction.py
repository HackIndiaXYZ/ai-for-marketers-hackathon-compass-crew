"""
ROI Prediction Module for PainToAd AI.

Calculates estimated marketing return-on-investment (ROI), projected revenue,
customer acquisition costs (CAC), budget utilization efficiency, and temporal forecasting metrics.
"""

import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ROIRequest(BaseModel):
    """Input payload for ROI forecasting."""
    total_budget: float = Field(..., gt=0.0, description="Total campaign budget in USD")
    target_channel: str = Field("Meta Ads", description="Marketing channel")
    estimated_impressions: float = Field(..., gt=0.0, description="Projected impression reach")
    predicted_ctr_pct: float = Field(..., gt=0.0, le=100.0, description="Predicted Click-Through Rate %")
    conversion_rate_pct: float = Field(2.5, gt=0.0, le=100.0, description="Landing page conversion rate %")
    average_order_value: float = Field(150.0, gt=0.0, description="Average revenue per customer/order in USD")
    campaign_duration_days: int = Field(30, gt=0, description="Campaign run duration in days")


class ROIForecastPoint(BaseModel):
    """Single period forecasting point."""
    day: int
    cumulative_spend: float
    cumulative_revenue: float
    cumulative_conversions: int
    net_profit: float


class ROIPredictionResponse(BaseModel):
    """Complete ROI prediction output payload."""
    total_budget: float
    predicted_revenue: float
    predicted_net_profit: float
    roi_multiplier: float = Field(..., description="ROI ratio (e.g. 2.5x means 250% return)")
    roi_percentage: float = Field(..., description="Net ROI %")
    customer_acquisition_cost: float = Field(..., description="Estimated CAC in USD")
    total_conversions: int
    cost_per_click: float
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    forecast_timeline: List[ROIForecastPoint]
    optimization_note: str


class ROIPredictor:
    """
    ROI Predictor calculating financial projections, conversion funnels,
    budget efficiency, and forecast timelines.
    """

    CHANNEL_COST_MULTIPLIERS: Dict[str, float] = {
        "Meta Ads": 1.0,
        "Google Ads": 1.15,
        "LinkedIn Ads": 1.85,
        "Email Marketing": 0.35,
        "TikTok Ads": 0.85
    }

    def __init__(self) -> None:
        """Initialize ROIPredictor."""
        logger.info("ROIPredictor initialized.")

    def calculate_roi(self, request: ROIRequest) -> ROIPredictionResponse:
        """
        Calculate expected ROI metrics and build temporal forecast timeline.

        Args:
            request: ROIRequest object.

        Returns:
            ROIPredictionResponse object.
        """
        try:
            cost_factor = self.CHANNEL_COST_MULTIPLIERS.get(request.target_channel, 1.0)

            # Clicks and Conversion Funnel
            total_clicks = int(request.estimated_impressions * (request.predicted_ctr_pct / 100.0))
            conversions = int(total_clicks * (request.conversion_rate_pct / 100.0))

            # Revenue & Financial Calculations
            gross_revenue = conversions * request.average_order_value
            net_profit = gross_revenue - request.total_budget

            roi_multiplier = round(gross_revenue / max(request.total_budget, 1.0), 2)
            roi_percentage = round(((gross_revenue - request.total_budget) / max(request.total_budget, 1.0)) * 100.0, 2)

            cac = round(request.total_budget / max(conversions, 1), 2)
            cpc = round(request.total_budget / max(total_clicks, 1), 2)

            # Confidence score calculation
            confidence = min(0.55 + (request.estimated_impressions / 1000000.0) * 0.2, 0.92)
            confidence = round(confidence, 2)

            # Timeline Forecast (daily ramp-up)
            timeline: List[ROIForecastPoint] = []
            daily_spend = request.total_budget / request.campaign_duration_days

            for day in range(1, request.campaign_duration_days + 1):
                progress = day / request.campaign_duration_days
                # Non-linear conversion ramp-up curve
                ramp_factor = progress ** 1.1
                cum_spend = round(daily_spend * day, 2)
                cum_conversions = int(conversions * ramp_factor)
                cum_revenue = round(cum_conversions * request.average_order_value, 2)
                cum_profit = round(cum_revenue - cum_spend, 2)

                timeline.append(ROIForecastPoint(
                    day=day,
                    cumulative_spend=cum_spend,
                    cumulative_revenue=cum_revenue,
                    cumulative_conversions=cum_conversions,
                    net_profit=cum_profit
                ))

            # Optimization Note
            if roi_multiplier >= 3.0:
                note = f"High-performing campaign! Excellent return potential on {request.target_channel}."
            elif roi_multiplier >= 1.5:
                note = f"Solid profitability expected. Consider increasing conversion rate to unlock 3x+ ROI."
            else:
                note = f"Low or negative ROI risk on {request.target_channel}. Improve CTR or lower CAC."

            return ROIPredictionResponse(
                total_budget=request.total_budget,
                predicted_revenue=round(gross_revenue, 2),
                predicted_net_profit=round(net_profit, 2),
                roi_multiplier=roi_multiplier,
                roi_percentage=roi_percentage,
                customer_acquisition_cost=cac,
                total_conversions=conversions,
                cost_per_click=cpc,
                confidence_score=confidence,
                forecast_timeline=timeline,
                optimization_note=note
            )

        except Exception as e:
            logger.error(f"Failed to execute ROI calculation: {e}")
            raise RuntimeError(f"ROI calculation execution error: {e}") from e


if __name__ == "__main__":
    predictor = ROIPredictor()
    req = ROIRequest(
        total_budget=5000.0,
        target_channel="Meta Ads",
        estimated_impressions=250000,
        predicted_ctr_pct=2.1,
        conversion_rate_pct=3.0,
        average_order_value=120.0
    )
    res = predictor.calculate_roi(req)
    print(res.model_dump_json(indent=2))
