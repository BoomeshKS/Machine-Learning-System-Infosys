from app.schemas import RiskInput

def calculate_risk(data: RiskInput) -> dict:

    d = data.model_dump()

    financial = (6 - d["budget_adequacy"]) / 5 * 100
    market = (6 - d["market_validation"]) / 5 * 100
    technical = (6 - d["technical_readiness"]) / 5 * 100
    operational = (6 - d["team_experience"] + 6 - d["resource_availability"]) / 10 * 100
    competition_regulatory = (
        d["competition_intensity"] + d["regulatory_complexity"] - 2
    ) / 8 * 100

    overall = (
        financial * 0.20
        + market * 0.25
        + technical * 0.20
        + operational * 0.20
        + competition_regulatory * 0.15
    )
    overall = round(overall, 2)
    level = "Low" if overall < 35 else "Medium" if overall < 65 else "High"

    return {
        "financial_risk": round(financial, 2),
        "market_risk": round(market, 2),
        "technical_risk": round(technical, 2),
        "operational_risk": round(operational, 2),
        "competition_regulatory_risk": round(competition_regulatory, 2),
        "overall_risk_score": overall,
        "risk_level": level,
        "success_probability_indicator": round(100 - overall, 2),
        "input_data": d,
    }
