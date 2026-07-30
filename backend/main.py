"""
PainToAd AI Backend

Main FastAPI Application

Connects frontend requests
with the complete AI pipeline.
"""


from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from typing import List


from backend.agents.orchestrator import (
    PainToAdOrchestrator
)



# ======================================================
# FastAPI Application
# ======================================================

app = FastAPI(

    title="PainToAd AI",

    description=
    "AI Marketing Intelligence Platform",

    version="1.0.0"

)



# ======================================================
# CORS Configuration
# ======================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:3000"

    ],

    allow_credentials=True,

    allow_methods=[

        "*"

    ],

    allow_headers=[

        "*"

    ],

)



# ======================================================
# Initialize AI Pipeline
# ======================================================

pipeline = PainToAdOrchestrator()



# ======================================================
# Request Models
# ======================================================


class Review(BaseModel):

    text: str

    source: str



class AnalyzeRequest(BaseModel):

    business_topic: str

    reviews: List[Review]



# ======================================================
# Health Check
# ======================================================


@app.get("/")
def home():

    return {

        "status": "running",

        "service": "PainToAd AI",

        "version": "1.0.0"

    }



# ======================================================
# AI Pipeline Status
# ======================================================


@app.get("/api/status")
def pipeline_status():

    return {


        "agents": [

            {

                "name":
                "Customer Voice Agent",

                "status":
                "ready"

            },


            {

                "name":
                "Pain Analysis Agent",

                "status":
                "ready"

            },


            {

                "name":
                "Persona Agent",

                "status":
                "ready"

            },


            {

                "name":
                "Campaign Agent",

                "status":
                "ready"

            },


            {

                "name":
                "Optimization Agent",

                "status":
                "ready"

            },


            {

                "name":
                "ROI Agent",

                "status":
                "ready"

            }

        ]

    }



# ======================================================
# Main Analyze Endpoint
# ======================================================


@app.post("/api/analyze")
def analyze_business(

    request: AnalyzeRequest

):

    try:


        reviews = [

            {

                "text":
                review.text,


                "source":
                review.source

            }

            for review in request.reviews

        ]


        result = pipeline.run(

            business_topic=
            request.business_topic,


            reviews=
            reviews

        )



        return {


            "success":
            True,


            "data":
            result


        }



    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail={

                "error":
                str(e),

                "message":
                "AI pipeline execution failed"

            }

        )