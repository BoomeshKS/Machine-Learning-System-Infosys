import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_market_analysis(project):

    prompt = f"""
    You are an expert market research analyst.

    Analyse the following startup/project idea.

    Project Name: {project.project_name}

    Industry: {project.industry}

    Business Model: {project.business_model}

    Target Market: {project.target_market}

    Budget: {project.budget}

    Description: {project.description}

    Objectives: {project.objectives}

    Existing Competitors: {project.competitors}

    Generate a detailed market analysis.

    Return ONLY valid JSON using this structure:

    {{
        "market_overview": "Market overview",
        "target_customers": "Target customers",
        "market_opportunities": [
            "Opportunity 1",
            "Opportunity 2"
        ],
        "market_challenges": [
            "Challenge 1",
            "Challenge 2"
        ],
        "competitors": [
            {{
                "name": "Competitor name",
                "product": "Product description",
                "comparison": "Comparison with our project"
            }}
        ],
        "industry_trends": [
            "Trend 1",
            "Trend 2"
        ]
    }}

    Do not invent market statistics or competitor facts.
    If information is unavailable, clearly mention that.
    """

    response = client.models.generate_content(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-2.0-flash"
        ),
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)