from dataclasses import dataclass

@dataclass
class RiskReport:
    score: int                  # 0–100
    level: str                  # Low / Moderate / High / Critical
    breakdown: dict             # what contributed to the score
    recommendations: list[str]  # actionable advice


def calculate_risk(
    platforms_found: list[dict],
    breaches: list[dict],
    pastes: list[dict],
) -> RiskReport:

    score = 0
    breakdown = {}
    recommendations = []

    # ── Platform exposure ──────────────────────────────────
    platform_count = len(platforms_found)
    platform_points = min(platform_count * 5, 30)   # cap at 30
    score += platform_points
    breakdown["platforms"] = {
        "count": platform_count,
        "points": platform_points,
        "detail": f"Found on {platform_count} platforms"
    }

    if platform_count >= 10:
        recommendations.append(
            "You have a large platform footprint. Audit and delete unused accounts."
        )

    # ── Username reuse ─────────────────────────────────────
    # If the same username appears on many sites, flag it
    if platform_count >= 5:
        reuse_points = 15
        score += reuse_points
        breakdown["username_reuse"] = {
            "points": reuse_points,
            "detail": "Same username found on 5+ platforms"
        }
        recommendations.append(
            "Consider using different usernames per platform to reduce traceability."
        )

    # ── Breach exposure ────────────────────────────────────
    breach_count = len(breaches)
    breach_points = 0

    if breach_count > 0:
        breach_points += 20    # base: email in at least one breach
        score += 20
        breakdown["breach_email"] = {
            "points": 20,
            "detail": f"Email found in {breach_count} breach(es)"
        }
        recommendations.append(
            "Your email appears in data breaches. Use unique emails per service."
        )

    # Password exposed in any breach?
    password_breaches = [
        b for b in breaches
        if "Passwords" in b.get("data_classes", [])
    ]
    if password_breaches:
        score += 30
        breakdown["breach_password"] = {
            "points": 30,
            "detail": f"Password exposed in {len(password_breaches)} breach(es)"
        }
        recommendations.append(
            "Your password was exposed. Change all passwords and enable 2FA immediately."
        )

    # ── Paste exposure ─────────────────────────────────────
    if pastes:
        paste_points = min(len(pastes) * 5, 20)
        score += paste_points
        breakdown["pastes"] = {
            "points": paste_points,
            "detail": f"Email found in {len(pastes)} public paste(s)"
        }
        recommendations.append(
            "Your email was found in public pastes. Monitor for spam and phishing."
        )

    # ── Sensitive breach ───────────────────────────────────
    sensitive = [b for b in breaches if b.get("is_sensitive")]
    if sensitive:
        score += 10
        breakdown["sensitive_breach"] = {
            "points": 10,
            "detail": f"Involved in {len(sensitive)} sensitive breach(es)"
        }

    # ── Cap and label ──────────────────────────────────────
    score = min(score, 100)

    if score <= 25:
        level = "Low"
    elif score <= 50:
        level = "Moderate"
    elif score <= 75:
        level = "High"
    else:
        level = "Critical"

    if not recommendations:
        recommendations.append("No immediate actions required. Keep monitoring.")

    return RiskReport(
        score=score,
        level=level,
        breakdown=breakdown,
        recommendations=recommendations,
    )
