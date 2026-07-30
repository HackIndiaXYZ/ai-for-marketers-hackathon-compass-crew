"""
ROI Intelligence Agent
======================

Combines ROI predictions with Gemini-generated business insights.

Current Mode:
-------------
Analytics models are temporarily mocked.

Reason:
-------
The analytics module is maintained separately.
This agent remains independent for AI workflow testing.

Pipeline

Optimization Agent
        │
        ▼
Mock CTR Prediction
Mock ROI Prediction
Mock Budget Allocation
        │
        ▼
Gemini Business Explanation
        │
        ▼
Frontend
"""


from backend.ai.gemini import gemini
from backend.ai.prompts import roi_prompt



# ============================================================
# Temporary Mock Analytics Functions
# Replace later when analytics team completes ML modules
# ============================================================


def predict_ctr(campaign: dict) -> dict:
    """
    Temporary CTR prediction placeholder.
    """

    return {
        "ctr": 0.05,
        "ctr_prediction": "Medium",
    }



def predict_roi(campaign: dict) -> dict:
    """
    Temporary ROI prediction placeholder.
    """

    return {
        "roi": 2.5,
        "roi_prediction": "Positive",
    }



def allocate_budget(campaign: dict) -> dict:
    """
    Temporary budget allocation placeholder.
    """

    return {
        "budget_percentage": 100,
    }



# ============================================================
# ROI Agent
# ============================================================


class ROIAgent:
    """
    ROI Intelligence Agent

    Uses:
    - Campaign optimization output
    - Temporary prediction layer
    - Gemini for business interpretation
    """

    def __init__(self):
        pass



    def run(self, optimization_output: dict) -> dict:
        """
        Run ROI intelligence pipeline.

        Parameters
        ----------
        optimization_output : dict

        Returns
        -------
        dict
        """


        topic = optimization_output["business_topic"]

        campaigns = optimization_output["optimized_campaigns"]

        predictions = []


        for campaign in campaigns:


            # -----------------------------------------
            # Prediction Layer
            # -----------------------------------------

            ctr_prediction = predict_ctr(campaign)

            roi_prediction = predict_roi(campaign)

            budget = allocate_budget(campaign)



            # -----------------------------------------
            # Gemini Business Explanation
            # -----------------------------------------

            prompt = roi_prompt(
                campaign=campaign,
                ctr_prediction=ctr_prediction,
                roi_prediction=roi_prediction,
                budget=budget,
            )


            explanation = gemini.generate_json(prompt)



            predictions.append(
                {
                    **campaign,

                    **ctr_prediction,

                    **roi_prediction,

                    **budget,


                    "executive_summary": explanation.get(
                        "executive_summary",
                        "",
                    ),

                    "business_summary": explanation.get(
                        "business_summary",
                        "",
                    ),

                    "kpis": explanation.get(
                        "kpis",
                        [],
                    ),

                    "risk_analysis": explanation.get(
                        "risk_analysis",
                        {},
                    ),

                    "recommendation": explanation.get(
                        "recommendation",
                        "",
                    ),

                    "confidence": explanation.get(
                        "confidence",
                        0.0,
                    ),
                }
            )



        return {
            "business_topic": topic,
            "campaign_predictions": predictions,
        }