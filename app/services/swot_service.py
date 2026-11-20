import json
import os
from typing import Any
from app.models import Project

def _rule_based_swot(project: Project) -> dict[str, Any]:
    description = project.description.lower()
    
    strengths = ["The project has a defined concept and description."]
    weaknesses = ["The proposal may need more detailed cost, timeline, and execution assumptions."]
    opportunities = ["Validate demand with target users and explore partnerships."]
    threats = ["Competitors, changing customer needs, and execution delays may affect outcomes."]

    if project.budget is not None and project.budget > 0:
        strengths.append("A project budget has been specified.")
    else:
        weaknesses.append("A budget has not been specified.")

    if project.target_market:
        strengths.append(f"A target market has been identified: {project.target_market}.")
    else:
        weaknesses.append("The target market has not been clearly specified.")

    if any(word in description for word in ["ai", "automation", "machine learning", "artificial intelligence"]):
        opportunities.append("The use of AI or automation may create scope for process improvements.")
    if project.industry_sector:
        opportunities.append(f"Research sector-specific trends in {project.industry_sector}.")
    if project.business_model:
        strengths.append(f"The proposed business model is identified as {project.business_model}.")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "opportunities": opportunities,
        "threats": threats,
        "provider": "rules",
    }

def generate_swot(project: Project) -> dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _rule_based_swot(project)

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        prompt = f"""
Create a concise, evidence-aware SWOT analysis for this project.
Return ONLY valid JSON with four keys: strengths, weaknesses, opportunities, threats.
Each value must be an array of 3 to 5 short strings. Do not invent market statistics.
If information is missing, state it as an assumption or validation need.

Project name: {project.project_name}
Project type: {project.project_type}
Industry: {project.industry_sector or "Not provided"}
Business model: {project.business_model or "Not provided"}
Budget: {project.budget if project.budget is not None else "Not provided"}
Target market: {project.target_market or "Not provided"}
Description: {project.description}
"""
        response = client.models.generate_content(model=model, contents=prompt)
        raw = response.text.strip()
        raw = raw.removeprefix("```json").removesuffix("```").strip()
        parsed = json.loads(raw)
        required = ["strengths", "weaknesses", "opportunities", "threats"]
        if not all(isinstance(parsed.get(k), list) and parsed[k] for k in required):
            raise ValueError("Gemini returned an invalid SWOT structure")
        return {**{k: [str(x) for x in parsed[k][:5]] for k in required}, "provider": "gemini"}
    except Exception:
        # Keep the API usable if Gemini is unavailable or returns invalid output.
        return _rule_based_swot(project)
