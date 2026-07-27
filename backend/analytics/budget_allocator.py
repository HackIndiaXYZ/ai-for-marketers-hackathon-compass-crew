"""
Budget Allocator Module for PainToAd AI.

Provides constrained optimization for marketing campaign budget distribution across channels
(e.g., Meta, Google Ads, LinkedIn, Email) to maximize overall portfolio ROI and conversions.
"""

import logging
from typing import Dict, List, Optional
import numpy as np
from pydantic import BaseModel, Field
from scipy.optimize import minimize

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChannelConstraint(BaseModel):
    """Specific budget constraints per marketing channel."""
    min_allocation_pct: float = Field(0.0, ge=0.0, le=100.0)
    max_allocation_pct: float = Field(100.0, ge=0.0, le=100.0)
    historical_roi_multiplier: float = Field(1.5, gt=0.0)


class BudgetAllocationRequest(BaseModel):
    """Payload for budget allocation request."""
    total_budget: float = Field(..., gt=0.0, description="Total budget in USD to distribute")
    channels: List[str] = Field(
        default=["Meta Ads", "Google Ads", "LinkedIn Ads", "Email Marketing"],
        description="Target marketing channels"
    )
    constraints: Optional[Dict[str, ChannelConstraint]] = None


class ChannelAllocationDetail(BaseModel):
    """Allocated spend details for a single channel."""
    channel_name: str
    allocated_amount: float
    percentage_of_budget: float
    expected_roi_multiplier: float
    expected_revenue: float
    estimated_conversions: int


class BudgetAllocationResponse(BaseModel):
    """Result payload from budget optimization engine."""
    total_budget: float
    optimized_revenue: float
    blended_roi_multiplier: float
    channel_allocations: List[ChannelAllocationDetail]
    spending_recommendation: str


class BudgetAllocator:
    """
    Budget Allocator optimizing marketing spend using SciPy SLSQP nonlinear programming
    to maximize revenue subject to budget and channel percentage constraints.
    """

    DEFAULT_CHANNEL_METRICS: Dict[str, Dict[str, float]] = {
        "Meta Ads": {"roi": 2.2, "cac": 45.0},
        "Google Ads": {"roi": 2.8, "cac": 55.0},
        "LinkedIn Ads": {"roi": 1.6, "cac": 120.0},
        "Email Marketing": {"roi": 4.5, "cac": 15.0},
        "TikTok Ads": {"roi": 1.9, "cac": 35.0}
    }

    def __init__(self) -> None:
        """Initialize BudgetAllocator."""
        logger.info("BudgetAllocator initialized.")

    def optimize_allocation(self, request: BudgetAllocationRequest) -> BudgetAllocationResponse:
        """
        Execute SLSQP optimization to maximize total expected portfolio revenue.

        Args:
            request: BudgetAllocationRequest object.

        Returns:
            BudgetAllocationResponse object.
        """
        try:
            channels = request.channels
            n_channels = len(channels)
            if n_channels == 0:
                raise ValueError("At least one marketing channel must be specified.")

            total_budget = request.total_budget

            # Extract ROI weights per channel
            rois = []
            cacs = []
            for ch in channels:
                user_constraint = request.constraints.get(ch) if request.constraints else None
                if user_constraint:
                    r = user_constraint.historical_roi_multiplier
                    c = 50.0
                else:
                    info = self.DEFAULT_CHANNEL_METRICS.get(ch, {"roi": 2.0, "cac": 50.0})
                    r = info["roi"]
                    c = info["cac"]
                rois.append(r)
                cacs.append(c)

            rois_arr = np.array(rois)

            # Define objective function (Minimize negative revenue with diminishing returns log scaling)
            def objective(x):
                # Diminishing returns: revenue = sum(roi * x^0.85)
                revenue = np.sum(rois_arr * (x ** 0.85))
                return -revenue

            # Constraint: Sum of allocations == total_budget
            def budget_constraint(x):
                return np.sum(x) - total_budget

            constraints = [{'type': 'eq', 'fun': budget_constraint}]

            # Bounds per channel
            bounds = []
            for i, ch in enumerate(channels):
                user_c = request.constraints.get(ch) if request.constraints else None
                min_val = (user_c.min_allocation_pct / 100.0 * total_budget) if user_c else 0.05 * total_budget
                max_val = (user_c.max_allocation_pct / 100.0 * total_budget) if user_c else 0.70 * total_budget
                bounds.append((min_val, max_val))

            # Initial equal split
            x0 = np.ones(n_channels) * (total_budget / n_channels)

            # Run scipy minimize optimization
            res = minimize(
                objective,
                x0,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )

            if res.success:
                allocations = res.x
            else:
                logger.warning(f"SciPy optimization did not converge perfectly ({res.message}). Using normalized weights.")
                allocations = (rois_arr / np.sum(rois_arr)) * total_budget

            # Build channel details
            details: List[ChannelAllocationDetail] = []
            total_revenue = 0.0

            for i, ch in enumerate(channels):
                amt = round(float(allocations[i]), 2)
                pct = round((amt / total_budget) * 100.0, 2)
                ch_roi = rois[i]
                exp_rev = round(amt * ch_roi, 2)
                total_revenue += exp_rev
                est_conv = int(amt / max(cacs[i], 1.0))

                details.append(ChannelAllocationDetail(
                    channel_name=ch,
                    allocated_amount=amt,
                    percentage_of_budget=pct,
                    expected_roi_multiplier=ch_roi,
                    expected_revenue=exp_rev,
                    estimated_conversions=est_conv
                ))

            blended_roi = round(total_revenue / total_budget, 2)

            top_channel = max(details, key=lambda d: d.allocated_amount)
            rec = f"Allocate {top_channel.percentage_of_budget}% of budget to {top_channel.channel_name} to leverage high ROI multipliers."

            return BudgetAllocationResponse(
                total_budget=total_budget,
                optimized_revenue=round(total_revenue, 2),
                blended_roi_multiplier=blended_roi,
                channel_allocations=details,
                spending_recommendation=rec
            )

        except Exception as e:
            logger.error(f"Error during budget optimization: {e}")
            raise RuntimeError(f"Budget allocation execution error: {e}") from e


if __name__ == "__main__":
    allocator = BudgetAllocator()
    req = BudgetAllocationRequest(
        total_budget=10000.0,
        channels=["Meta Ads", "Google Ads", "LinkedIn Ads", "Email Marketing"]
    )
    resp = allocator.optimize_allocation(req)
    print(resp.model_dump_json(indent=2))
