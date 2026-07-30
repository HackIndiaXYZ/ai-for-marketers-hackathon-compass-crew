"""
PainToAd AI Orchestrator
========================

Coordinates the complete multi-agent AI workflow.

Pipeline

Customer Voice
        ↓
Pain Analysis
        ↓
Persona
        ↓
Campaign
        ↓
Optimization
        ↓
ROI

This class contains NO AI logic.

Its responsibility is ONLY to coordinate
the individual AI agents.
"""

from datetime import datetime, timezone
import time

from backend.agents.customer_voice_agent import CustomerVoiceAgent
from backend.agents.pain_analysis_agent import PainAnalysisAgent
from backend.agents.persona_agent import PersonaAgent
from backend.agents.campaign_agent import CampaignAgent
from backend.agents.optimization_agent import OptimizationAgent
from backend.agents.roi_agent import ROIAgent


class PainToAdOrchestrator:
    """
    Main AI Pipeline Coordinator.
    """

    def __init__(self):

        self.customer_voice = CustomerVoiceAgent()

        self.pain_analysis = PainAnalysisAgent()

        self.persona = PersonaAgent()

        self.campaign = CampaignAgent()

        self.optimization = OptimizationAgent()

        self.roi = ROIAgent()

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------

    @staticmethod
    def _completed(workflow, agent_name):
        workflow.append(
            {
                "agent": agent_name,
                "status": "Completed",
            }
        )

    @staticmethod
    def _failed(workflow, agent_name):
        workflow.append(
            {
                "agent": agent_name,
                "status": "Failed",
            }
        )

    # ---------------------------------------------------------
    # Pipeline
    # ---------------------------------------------------------

    def run(
        self,
        business_topic: str,
        reviews: list,
    ) -> dict:

        workflow = []

        start_time = time.time()

        try:

            # ==================================================
            # Customer Voice Agent
            # ==================================================

            customer_voice_output = self.customer_voice.run(
                topic=business_topic,
                reviews=reviews,
            )

            self._completed(
                workflow,
                "Customer Voice",
            )

        except Exception as e:

            self._failed(
                workflow,
                "Customer Voice",
            )

            return {
                "success": False,
                "stage": "Customer Voice",
                "error": str(e),
                "workflow": workflow,
            }

        try:

            # ==================================================
            # Pain Analysis Agent
            # ==================================================

            pain_output = self.pain_analysis.run(
                customer_voice_output,
            )

            self._completed(
                workflow,
                "Pain Analysis",
            )

        except Exception as e:

            self._failed(
                workflow,
                "Pain Analysis",
            )

            return {
                "success": False,
                "stage": "Pain Analysis",
                "error": str(e),
                "workflow": workflow,
            }

        try:

            # ==================================================
            # Persona Agent
            # ==================================================

            persona_output = self.persona.run(
                pain_output,
            )

            self._completed(
                workflow,
                "Persona",
            )

        except Exception as e:

            self._failed(
                workflow,
                "Persona",
            )

            return {
                "success": False,
                "stage": "Persona",
                "error": str(e),
                "workflow": workflow,
            }

        try:

            # ==================================================
            # Campaign Agent
            # ==================================================

            campaign_output = self.campaign.run(
                persona_output,
            )

            self._completed(
                workflow,
                "Campaign",
            )

        except Exception as e:

            self._failed(
                workflow,
                "Campaign",
            )

            return {
                "success": False,
                "stage": "Campaign",
                "error": str(e),
                "workflow": workflow,
            }

        try:

            # ==================================================
            # Optimization Agent
            # ==================================================

            optimization_output = self.optimization.run(
                campaign_output,
            )

            self._completed(
                workflow,
                "Optimization",
            )

        except Exception as e:

            self._failed(
                workflow,
                "Optimization",
            )

            return {
                "success": False,
                "stage": "Optimization",
                "error": str(e),
                "workflow": workflow,
            }

        try:

            # ==================================================
            # ROI Agent
            # ==================================================

            roi_output = self.roi.run(
                optimization_output,
            )

            self._completed(
                workflow,
                "ROI",
            )

        except Exception as e:

            self._failed(
                workflow,
                "ROI",
            )

            return {
                "success": False,
                "stage": "ROI",
                "error": str(e),
                "workflow": workflow,
            }

        execution_time = round(
            time.time() - start_time,
            2,
        )

        metadata = {
            "ai_model": "Gemini 2.5 Flash",
            "pipeline_version": "1.0.0",
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        return {

            "success": True,

            "business_topic": business_topic,

            "customer_voice": customer_voice_output,

            "pain_analysis": pain_output,

            "personas": persona_output,

            "campaigns": campaign_output,

            "optimization": optimization_output,

            "roi": roi_output,

            "workflow": workflow,

            "execution_time": f"{execution_time} seconds",

            "metadata": metadata,
        }