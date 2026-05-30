import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
OUTPUTS = ANALYSIS / "outputs"
DOCS = ROOT / "docs" / "images"

random.seed(5292026)


OPPORTUNITIES = [
    {
        "feature_id": "AIP001",
        "feature_name": "Daily resource planner",
        "domain": "Productivity",
        "target_segment": "Busy professionals",
        "ai_method": "Recommendation system",
        "user_problem": "Users need one ranked plan that blends calendar pressure, tasks, document deadlines, and personal routines.",
        "primary_kpi": "Weekly planned task completion",
        "owner": "Product and ML",
        "roadmap_lane": "Now",
        "base_reach": 185000,
        "business_value": 95,
        "user_evidence": 92,
        "effort": 58,
        "model_complexity": 72,
        "privacy_risk": 55,
        "data_quality": 86,
        "sensitivity": "Moderate",
        "launch_gate": "Experiment ready",
    },
    {
        "feature_id": "AIP002",
        "feature_name": "Entrepreneur launch checklist",
        "domain": "Entrepreneurship",
        "target_segment": "Solo founders",
        "ai_method": "NLP planning assistant",
        "user_problem": "First-time builders need a practical sequence for market research, launch assets, and financial setup.",
        "primary_kpi": "Checklist activation rate",
        "owner": "Product and Design",
        "roadmap_lane": "Now",
        "base_reach": 112000,
        "business_value": 90,
        "user_evidence": 89,
        "effort": 47,
        "model_complexity": 62,
        "privacy_risk": 48,
        "data_quality": 84,
        "sensitivity": "Moderate",
        "launch_gate": "PRD ready",
    },
    {
        "feature_id": "AIP003",
        "feature_name": "Document to action extractor",
        "domain": "Documents",
        "target_segment": "Mobile office users",
        "ai_method": "NLP extraction",
        "user_problem": "Scanned PDFs, receipts, and forms often contain dates and obligations that never become tasks.",
        "primary_kpi": "Extracted action acceptance",
        "owner": "Product, ML, and Data",
        "roadmap_lane": "Now",
        "base_reach": 160000,
        "business_value": 88,
        "user_evidence": 86,
        "effort": 69,
        "model_complexity": 78,
        "privacy_risk": 74,
        "data_quality": 79,
        "sensitivity": "High",
        "launch_gate": "Privacy review",
    },
    {
        "feature_id": "AIP004",
        "feature_name": "Smart task decomposition",
        "domain": "Productivity",
        "target_segment": "Students and professionals",
        "ai_method": "NLP planning assistant",
        "user_problem": "Large goals stall because users do not know the next concrete action or realistic sequence.",
        "primary_kpi": "Goal to first action rate",
        "owner": "Product and Design",
        "roadmap_lane": "Now",
        "base_reach": 174000,
        "business_value": 91,
        "user_evidence": 88,
        "effort": 42,
        "model_complexity": 58,
        "privacy_risk": 44,
        "data_quality": 88,
        "sensitivity": "Low",
        "launch_gate": "Experiment ready",
    },
    {
        "feature_id": "AIP005",
        "feature_name": "Cross-app morning brief",
        "domain": "Ecosystem",
        "target_segment": "Subscription power users",
        "ai_method": "Recommendation system",
        "user_problem": "Users miss value across apps because tasks, habits, documents, spend, and learning reminders are fragmented.",
        "primary_kpi": "Multi-app weekly engagement",
        "owner": "Growth Product",
        "roadmap_lane": "Now",
        "base_reach": 142000,
        "business_value": 94,
        "user_evidence": 82,
        "effort": 63,
        "model_complexity": 70,
        "privacy_risk": 68,
        "data_quality": 76,
        "sensitivity": "High",
        "launch_gate": "Consent copy",
    },
    {
        "feature_id": "AIP006",
        "feature_name": "Receipt and budget deadline advisor",
        "domain": "Finance",
        "target_segment": "Household planners",
        "ai_method": "Classification and forecasting",
        "user_problem": "Users forget subscription renewals, bill dates, and reimbursement tasks after scanning receipts or invoices.",
        "primary_kpi": "Avoided missed deadline rate",
        "owner": "Product, ML, and Compliance",
        "roadmap_lane": "Next",
        "base_reach": 96000,
        "business_value": 82,
        "user_evidence": 80,
        "effort": 72,
        "model_complexity": 75,
        "privacy_risk": 88,
        "data_quality": 73,
        "sensitivity": "High",
        "launch_gate": "Compliance review",
    },
    {
        "feature_id": "AIP007",
        "feature_name": "Learning plan generator",
        "domain": "Education",
        "target_segment": "Language learners",
        "ai_method": "Recommendation system",
        "user_problem": "Learners need an adaptive sequence that responds to weak skills, daily availability, and motivation dips.",
        "primary_kpi": "Seven day lesson streak",
        "owner": "Product and Data Science",
        "roadmap_lane": "Next",
        "base_reach": 121000,
        "business_value": 76,
        "user_evidence": 78,
        "effort": 55,
        "model_complexity": 65,
        "privacy_risk": 42,
        "data_quality": 85,
        "sensitivity": "Low",
        "launch_gate": "Experiment ready",
    },
    {
        "feature_id": "AIP008",
        "feature_name": "Habit recovery coach",
        "domain": "Wellness",
        "target_segment": "Habit builders",
        "ai_method": "NLP coaching assistant",
        "user_problem": "Users churn after broken streaks because the app does not help them recover without shame or overload.",
        "primary_kpi": "Recovered streak rate",
        "owner": "Product and Design",
        "roadmap_lane": "Next",
        "base_reach": 118000,
        "business_value": 74,
        "user_evidence": 83,
        "effort": 44,
        "model_complexity": 56,
        "privacy_risk": 66,
        "data_quality": 82,
        "sensitivity": "Moderate",
        "launch_gate": "Content safety",
    },
    {
        "feature_id": "AIP009",
        "feature_name": "Secure password task reminders",
        "domain": "Security",
        "target_segment": "Family admins",
        "ai_method": "Rules plus classification",
        "user_problem": "Users need privacy-preserving reminders for expiring credentials and shared account hygiene.",
        "primary_kpi": "Security task completion",
        "owner": "Security Product",
        "roadmap_lane": "Later",
        "base_reach": 78000,
        "business_value": 70,
        "user_evidence": 72,
        "effort": 66,
        "model_complexity": 48,
        "privacy_risk": 92,
        "data_quality": 70,
        "sensitivity": "High",
        "launch_gate": "Security review",
    },
    {
        "feature_id": "AIP010",
        "feature_name": "Image based plant care planner",
        "domain": "Utility",
        "target_segment": "Home care users",
        "ai_method": "Computer vision",
        "user_problem": "Users can identify plants but need a care plan that turns recognition into reminders and supply lists.",
        "primary_kpi": "Care plan save rate",
        "owner": "Product and ML",
        "roadmap_lane": "Later",
        "base_reach": 84000,
        "business_value": 66,
        "user_evidence": 71,
        "effort": 61,
        "model_complexity": 82,
        "privacy_risk": 32,
        "data_quality": 74,
        "sensitivity": "Low",
        "launch_gate": "Model eval",
    },
    {
        "feature_id": "AIP011",
        "feature_name": "Translation context memory",
        "domain": "Communication",
        "target_segment": "Travel and work users",
        "ai_method": "NLP personalization",
        "user_problem": "Repeated translations lose context when users move between travel, work, and learning situations.",
        "primary_kpi": "Repeat translation satisfaction",
        "owner": "Product and ML",
        "roadmap_lane": "Next",
        "base_reach": 136000,
        "business_value": 79,
        "user_evidence": 77,
        "effort": 52,
        "model_complexity": 64,
        "privacy_risk": 60,
        "data_quality": 81,
        "sensitivity": "Moderate",
        "launch_gate": "Consent copy",
    },
    {
        "feature_id": "AIP012",
        "feature_name": "Design brief to asset plan",
        "domain": "Creative",
        "target_segment": "Small business creators",
        "ai_method": "Generative assistant",
        "user_problem": "Creators can generate designs but struggle to convert campaign goals into an asset sequence.",
        "primary_kpi": "Asset plan completion",
        "owner": "Creative Product",
        "roadmap_lane": "Later",
        "base_reach": 90000,
        "business_value": 73,
        "user_evidence": 75,
        "effort": 67,
        "model_complexity": 80,
        "privacy_risk": 52,
        "data_quality": 72,
        "sensitivity": "Moderate",
        "launch_gate": "Brand safety",
    },
]

SIGNAL_SOURCES = [
    "App store review theme",
    "Support ticket cluster",
    "In-app survey",
    "User interview",
    "Competitive teardown",
    "Experiment note",
]

PRD_THEMES = [
    "Explain the recommendation",
    "Let users edit the plan",
    "Handle ambiguous inputs",
    "Ask consent before cross-app use",
    "Escalate low confidence outputs",
    "Instrument outcome quality",
]


def clamp(value, low, high):
    return max(low, min(high, value))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def opportunity_rows():
    return [
        {
            "feature_id": item["feature_id"],
            "feature_name": item["feature_name"],
            "domain": item["domain"],
            "target_segment": item["target_segment"],
            "ai_method": item["ai_method"],
            "user_problem": item["user_problem"],
            "primary_kpi": item["primary_kpi"],
            "owner": item["owner"],
            "roadmap_lane": item["roadmap_lane"],
            "sensitivity": item["sensitivity"],
            "launch_gate": item["launch_gate"],
        }
        for item in OPPORTUNITIES
    ]


def make_weekly_metrics():
    rows = []
    for item in OPPORTUNITIES:
        for week in range(1, 13):
            seasonal = math.sin(week / 12 * math.pi) * 4
            adoption = clamp(random.gauss(item["user_evidence"] * 0.72 + seasonal, 5), 30, 92)
            completion = clamp(random.gauss(item["data_quality"] * 0.82 - item["model_complexity"] * 0.09, 4), 42, 94)
            conversion_lift = clamp(random.gauss(item["business_value"] / 18, 1.2), 0.3, 8.9)
            retention_lift = clamp(random.gauss(item["user_evidence"] / 25, 1.0), 0.1, 7.4)
            accuracy = clamp(random.gauss(item["data_quality"] - item["model_complexity"] * 0.12, 3.2), 54, 94)
            hallucination = clamp(random.gauss(item["model_complexity"] * 0.10 + item["privacy_risk"] * 0.025, 1.1), 1.0, 14.5)
            latency = int(clamp(random.gauss(520 + item["model_complexity"] * 11, 110), 360, 1900))
            escalations = clamp(random.gauss(item["privacy_risk"] * 0.07 + item["model_complexity"] * 0.03, 0.8), 0.4, 13.0)
            rows.append(
                {
                    "week": f"2026-W{week:02d}",
                    "feature_id": item["feature_id"],
                    "active_users": int(random.gauss(item["base_reach"], item["base_reach"] * 0.08)),
                    "ai_completion_rate": round(completion, 1),
                    "subscription_conversion_lift_pp": round(conversion_lift, 2),
                    "retention_lift_pp": round(retention_lift, 2),
                    "model_accuracy": round(accuracy, 1),
                    "hallucination_rate": round(hallucination, 1),
                    "support_escalations_per_10k": round(escalations, 1),
                    "p95_latency_ms": latency,
                    "data_quality_score": round(clamp(random.gauss(item["data_quality"], 4), 50, 96), 1),
                }
            )
    return rows


def make_research_signals():
    rows = []
    counter = 1
    for item in OPPORTUNITIES:
        signal_count = random.randint(9, 16)
        for _ in range(signal_count):
            source = random.choice(SIGNAL_SOURCES)
            theme = random.choice(PRD_THEMES)
            sentiment = random.choice(["Positive", "Mixed", "Negative", "Request"])
            severity = random.choice(["Low", "Medium", "High"])
            evidence_weight = clamp(random.gauss(item["user_evidence"], 11), 38, 98)
            rows.append(
                {
                    "signal_id": f"SIG{counter:04d}",
                    "feature_id": item["feature_id"],
                    "source": source,
                    "theme": theme,
                    "sentiment": sentiment,
                    "severity": severity,
                    "evidence_weight": round(evidence_weight, 1),
                    "note": f"{source} highlights that {theme.lower()} matters for {item['target_segment'].lower()}.",
                }
            )
            counter += 1
    return rows


def make_model_evals():
    rows = []
    for item in OPPORTUNITIES:
        method = item["ai_method"]
        if "Computer vision" in method:
            eval_set = "Image recognition and plan generation"
        elif "Recommendation" in method:
            eval_set = "Ranking relevance and novelty"
        elif "Classification" in method:
            eval_set = "Deadline and intent classification"
        else:
            eval_set = "Prompt following and extraction"

        rows.append(
            {
                "feature_id": item["feature_id"],
                "eval_set": eval_set,
                "ai_method": method,
                "offline_quality_score": round(clamp(item["data_quality"] - item["model_complexity"] * 0.11 + random.gauss(0, 3), 48, 95), 1),
                "human_acceptance_rate": round(clamp(item["user_evidence"] - item["privacy_risk"] * 0.05 + random.gauss(0, 4), 45, 94), 1),
                "hallucination_or_error_rate": round(clamp(item["model_complexity"] * 0.13 + random.gauss(0, 1.4), 1.8, 17.5), 1),
                "fairness_gap_pp": round(clamp(random.gauss(item["privacy_risk"] * 0.045, 1.1), 0.2, 8.8), 1),
                "p95_latency_ms": int(clamp(random.gauss(590 + item["model_complexity"] * 10, 130), 390, 2050)),
                "model_readiness": round(clamp(item["data_quality"] * 0.45 + item["user_evidence"] * 0.35 - item["model_complexity"] * 0.12 - item["privacy_risk"] * 0.08 + 28, 35, 96), 1),
            }
        )
    return rows


def make_experiment_plans():
    rows = []
    for item in OPPORTUNITIES:
        sample = int(clamp(item["base_reach"] * random.uniform(0.08, 0.18), 6500, 28000))
        rows.append(
            {
                "feature_id": item["feature_id"],
                "experiment_name": f"{item['feature_name']} guided launch",
                "hypothesis": f"If {item['feature_name'].lower()} is introduced with transparent controls, {item['primary_kpi'].lower()} will improve without raising escalations.",
                "primary_metric": item["primary_kpi"],
                "guardrail_metric": "Support escalations and low confidence AI outputs",
                "sample_plan": f"{sample:,} eligible users",
                "minimum_detectable_lift": f"{round(random.uniform(2.5, 6.5), 1)} pp",
                "duration_days": random.choice([14, 21, 28]),
                "decision_rule": "Ship when lift clears threshold and guardrails stay within tolerance",
            }
        )
    return rows


def make_trust_controls():
    rows = []
    for item in OPPORTUNITIES:
        consent = "Required" if item["privacy_risk"] >= 58 else "Contextual notice"
        retention = "30 day rolling window" if item["sensitivity"] == "High" else "90 day rolling window"
        blocker = "Yes" if item["privacy_risk"] >= 82 or item["launch_gate"] in {"Compliance review", "Security review"} else "No"
        rows.append(
            {
                "feature_id": item["feature_id"],
                "data_sensitivity": item["sensitivity"],
                "consent_requirement": consent,
                "retention_policy": retention,
                "human_fallback": "Low confidence outputs route to editable draft",
                "monitoring_plan": "Weekly review of accuracy, escalation, latency, and opt out rate",
                "privacy_risk_score": item["privacy_risk"],
                "launch_blocker": blocker,
                "review_status": item["launch_gate"],
            }
        )
    return rows


def aggregate(opportunities, weekly, signals, evals, experiments, controls):
    weekly_by_feature = defaultdict(list)
    for row in weekly:
        weekly_by_feature[row["feature_id"]].append(row)

    signal_by_feature = defaultdict(list)
    for row in signals:
        signal_by_feature[row["feature_id"]].append(row)

    eval_by_feature = {row["feature_id"]: row for row in evals}
    experiment_by_feature = {row["feature_id"]: row for row in experiments}
    control_by_feature = {row["feature_id"]: row for row in controls}

    priority = []
    prd_cards = []
    model_queue = []
    experiment_readiness = []
    trust_queue = []

    for item in opportunities:
        feature_id = item["feature_id"]
        metrics = weekly_by_feature[feature_id]
        signal_rows = signal_by_feature[feature_id]
        latest = metrics[-1]
        avg_accuracy = sum(float(row["model_accuracy"]) for row in metrics) / len(metrics)
        avg_completion = sum(float(row["ai_completion_rate"]) for row in metrics) / len(metrics)
        avg_conversion = sum(float(row["subscription_conversion_lift_pp"]) for row in metrics) / len(metrics)
        avg_retention = sum(float(row["retention_lift_pp"]) for row in metrics) / len(metrics)
        avg_escalation = sum(float(row["support_escalations_per_10k"]) for row in metrics) / len(metrics)
        avg_latency = sum(float(row["p95_latency_ms"]) for row in metrics) / len(metrics)
        evidence = sum(float(row["evidence_weight"]) for row in signal_rows) / len(signal_rows)
        model = eval_by_feature[feature_id]
        control = control_by_feature[feature_id]
        experiment = experiment_by_feature[feature_id]
        impact_score = item["business_value"] * 0.35 + item["user_evidence"] * 0.25 + avg_conversion * 4.5 + avg_retention * 3.2
        risk_penalty = item["effort"] * 0.18 + item["privacy_risk"] * 0.22 + avg_escalation * 1.4
        readiness_bonus = float(model["model_readiness"]) * 0.24 + item["data_quality"] * 0.14
        priority_score = round(clamp(impact_score + readiness_bonus - risk_penalty, 1, 100), 1)
        confidence = round(clamp((evidence * 0.35 + item["data_quality"] * 0.25 + float(model["model_readiness"]) * 0.25 + avg_accuracy * 0.15) / 100, 0.35, 0.96), 2)
        rice_score = round(priority_score * confidence * math.sqrt(item["base_reach"] / 1000) / max(item["effort"], 1), 2)
        action = "Ship controlled beta" if priority_score >= 76 and control["launch_blocker"] == "No" else "Resolve launch gate" if priority_score >= 70 else "Keep in discovery"

        priority.append(
            {
                "feature_id": feature_id,
                "feature_name": item["feature_name"],
                "domain": item["domain"],
                "target_segment": item["target_segment"],
                "ai_method": item["ai_method"],
                "roadmap_lane": item["roadmap_lane"],
                "priority_score": priority_score,
                "rice_score": rice_score,
                "confidence": confidence,
                "active_users": latest["active_users"],
                "conversion_lift_pp": round(avg_conversion, 2),
                "retention_lift_pp": round(avg_retention, 2),
                "model_readiness": model["model_readiness"],
                "privacy_risk_score": item["privacy_risk"],
                "effort": item["effort"],
                "launch_gate": item["launch_gate"],
                "recommended_action": action,
                "user_problem": item["user_problem"],
                "primary_kpi": item["primary_kpi"],
                "owner": item["owner"],
            }
        )

        theme_counts = defaultdict(int)
        for row in signal_rows:
            theme_counts[row["theme"]] += 1
        top_theme = sorted(theme_counts.items(), key=lambda row: row[1], reverse=True)[0][0]
        prd_cards.append(
            {
                "requirement_id": f"PRD-{feature_id[-3:]}",
                "feature_id": feature_id,
                "feature_name": item["feature_name"],
                "theme": top_theme,
                "persona": item["target_segment"],
                "problem": item["user_problem"],
                "user_story": f"As a {item['target_segment'].lower()}, I want {item['feature_name'].lower()} to explain and adjust its plan",
                "acceptance_criteria": "Recommendation includes rationale, editable steps, confidence state, and a clear undo path.",
                "validation_plan": experiment["decision_rule"],
                "instrumentation": item["primary_kpi"],
                "evidence_source": signal_rows[0]["source"],
                "request_count": len(signal_rows),
                "severity": "High" if item["privacy_risk"] >= 70 or item["business_value"] >= 88 else "Medium",
                "prd_status": "Ready for grooming" if item["launch_gate"] in {"Experiment ready", "PRD ready"} else item["launch_gate"],
            }
        )

        model_queue.append(
            {
                "feature_id": feature_id,
                "feature_name": item["feature_name"],
                "ai_method": item["ai_method"],
                "eval_set": model["eval_set"],
                "offline_quality_score": model["offline_quality_score"],
                "human_acceptance_rate": model["human_acceptance_rate"],
                "error_rate": model["hallucination_or_error_rate"],
                "fairness_gap_pp": model["fairness_gap_pp"],
                "p95_latency_ms": model["p95_latency_ms"],
                "model_readiness": model["model_readiness"],
                "quality_decision": "Launch monitor" if float(model["model_readiness"]) >= 78 and float(model["hallucination_or_error_rate"]) < 10 else "Needs eval work",
            }
        )

        experiment_readiness.append(
            {
                "feature_id": feature_id,
                "feature_name": item["feature_name"],
                "domain": item["domain"],
                "hypothesis": experiment["hypothesis"],
                "primary_metric": experiment["primary_metric"],
                "guardrail_metric": experiment["guardrail_metric"],
                "sample_plan": experiment["sample_plan"],
                "minimum_detectable_lift": experiment["minimum_detectable_lift"],
                "duration_days": experiment["duration_days"],
                "decision_rule": experiment["decision_rule"],
                "experiment_status": "Ready" if priority_score >= 72 and control["launch_blocker"] == "No" else "Gate review",
            }
        )

        trust_queue.append(
            {
                "feature_id": feature_id,
                "feature_name": item["feature_name"],
                "data_sensitivity": control["data_sensitivity"],
                "consent_requirement": control["consent_requirement"],
                "retention_policy": control["retention_policy"],
                "human_fallback": control["human_fallback"],
                "monitoring_plan": control["monitoring_plan"],
                "privacy_risk_score": control["privacy_risk_score"],
                "launch_blocker": control["launch_blocker"],
                "review_status": control["review_status"],
            }
        )

    priority.sort(key=lambda row: row["priority_score"], reverse=True)
    prd_cards.sort(key=lambda row: row["request_count"], reverse=True)
    model_queue.sort(key=lambda row: row["model_readiness"], reverse=True)
    experiment_readiness.sort(key=lambda row: (row["experiment_status"], row["feature_name"]), reverse=True)
    trust_queue.sort(key=lambda row: row["privacy_risk_score"], reverse=True)

    summary = {
        "feature_count": len(opportunities),
        "top_feature": priority[0],
        "ready_experiments": sum(1 for row in experiment_readiness if row["experiment_status"] == "Ready"),
        "launch_blockers": sum(1 for row in trust_queue if row["launch_blocker"] == "Yes"),
        "avg_model_readiness": round(sum(float(row["model_readiness"]) for row in model_queue) / len(model_queue), 1),
        "avg_priority_score": round(sum(float(row["priority_score"]) for row in priority) / len(priority), 1),
    }

    payload = {
        "summary": summary,
        "priorityQueue": priority,
        "prdCards": prd_cards,
        "modelQuality": model_queue,
        "experimentReadiness": experiment_readiness,
        "trustReview": trust_queue,
        "weeklyMetrics": weekly,
    }

    return priority, prd_cards, model_queue, experiment_readiness, trust_queue, summary, payload


def write_docs(summary):
    top = summary["top_feature"]
    write_text(
        DATA / "README.md",
        """# Data Sources

All datasets are deterministic synthetic data for a public AI product management portfolio artifact. They do not represent any real company, user, app, subscription, model, or operating performance.

The synthetic data is modeled on a multi-app mobile subscription ecosystem with productivity, document, finance, education, wellness, communication, utility, creative, and security workflows. The generator uses a fixed random seed so the project is reproducible.

- `ai_opportunities.csv`: AI planner feature candidates with domain, user problem, KPI, owner, sensitivity, and launch gate.
- `weekly_product_metrics.csv`: Twelve weeks of synthetic usage, conversion, retention, model quality, latency, escalation, and data quality metrics.
- `research_signals.csv`: Synthetic app-review, support, survey, interview, competitive, and experiment evidence themes.
- `model_evaluations.csv`: Offline and human evaluation metrics for NLP, recommendation, classification, generative, and computer vision features.
- `experiment_plans.csv`: Experiment hypotheses, primary metrics, guardrails, sample plans, MDEs, and decision rules.
- `trust_controls.csv`: Consent, retention, fallback, monitoring, privacy risk, and launch blocker records.
""",
    )

    write_text(
        ROOT / "data_dictionary.md",
        """# Data Dictionary

| Table | Grain | Purpose |
|---|---|---|
| `ai_opportunities.csv` | AI feature candidate | Defines the product opportunity, user problem, AI method, KPI, roadmap lane, owner, and launch gate. |
| `weekly_product_metrics.csv` | Feature by week | Tracks synthetic adoption, conversion lift, retention lift, AI completion, model accuracy, latency, escalation, and data quality. |
| `research_signals.csv` | Evidence signal | Captures synthetic qualitative and market evidence used to shape PRD requirements. |
| `model_evaluations.csv` | Feature eval | Summarizes offline quality, human acceptance, error rate, fairness gap, latency, and readiness. |
| `experiment_plans.csv` | Feature experiment | Defines hypothesis, metric, guardrail, sample plan, detectable lift, duration, and ship rule. |
| `trust_controls.csv` | Feature trust review | Documents sensitivity, consent, retention, fallback, monitoring, privacy risk, blocker, and review state. |
| `analysis/outputs/priority_queue.csv` | Feature score | Ranks opportunities using impact, confidence, effort, model readiness, data quality, and privacy risk. |
""",
    )

    write_text(
        ANALYSIS / "analysis_plan.md",
        """# Analysis Plan

## Decision Question

Which AI planner capabilities should an AI product manager move from discovery into PRD, experiment, or launch review for a multi-app mobile subscription ecosystem?

## Inputs

1. Product opportunity metadata for each AI feature candidate.
2. Weekly synthetic product metrics for adoption, conversion lift, retention lift, model quality, latency, support escalation, and data quality.
3. User, support, market, and experiment evidence signals.
4. Model evaluation outputs for quality, acceptance, error rate, fairness gap, and readiness.
5. Experiment plans and trust controls.

## Scoring Logic

The priority score rewards business value, user evidence, conversion lift, retention lift, model readiness, and data quality. It penalizes implementation effort, privacy risk, and support escalation pressure. The RICE-style score adjusts priority by confidence, reachable audience, and effort.

## Review Cadence

- Product reviews the top queue and PRD cards weekly.
- Data science reviews model quality and error rates before experiment launch.
- Design validates explainability, editability, and fallback paths.
- Privacy and compliance review high-sensitivity workflows before rollout.
""",
    )

    write_text(
        ANALYSIS / "methodology.md",
        """# Methodology

The project uses deterministic synthetic data because public product telemetry, model evaluation data, and privacy review records do not exist for this exact product context.

The generator models a mobile subscription ecosystem with multiple app domains. Productivity and document workflows receive larger reachable audiences. Finance, security, and cross-app workflows carry higher privacy risk. Generative and computer vision workflows carry higher model complexity. Recommendation and task-planning workflows receive stronger near-term roadmap weights when user evidence and data quality are high.

The scoring model is intentionally transparent. It is not a production ML model. It is a product decision rubric that an AI product manager could explain in a roadmap review.
""",
    )

    write_text(
        ANALYSIS / "executive_findings.md",
        f"""# Executive Findings

## What I Analyzed

I generated and analyzed synthetic AI product data for {summary['feature_count']} planner capabilities across mobile productivity, documents, finance, education, wellness, security, communication, creative, utility, and subscription ecosystem workflows.

## Findings

- The highest ranked AI feature is `{top['feature_name']}` with a priority score of {top['priority_score']}.
- {summary['ready_experiments']} features are ready for controlled experiments after PRD review.
- {summary['launch_blockers']} features have trust, privacy, security, compliance, or consent blockers that should be resolved before scale.
- Average model readiness is {summary['avg_model_readiness']}, which means the artifact should balance roadmap ambition with eval and monitoring gates.

## Recommendation

Use the priority queue to select the next AI planner bet, then use the PRD, model quality, experiment, and trust surfaces to decide whether that bet should move to beta, stay in discovery, or enter launch gate remediation.
""",
    )

    write_text(
        ANALYSIS / "sql_checks.sql",
        """-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.
-- They are written as portable validation logic for review, not tied to a live warehouse.

-- Check 1: every opportunity has 12 weekly metric rows.
select
  feature_id,
  count(*) as week_count
from weekly_product_metrics
group by feature_id
having count(*) <> 12;

-- Check 2: no model readiness score falls outside the scoring range.
select *
from model_evaluations
where model_readiness < 0
   or model_readiness > 100;

-- Check 3: high privacy risk features must have explicit consent or review.
select *
from trust_controls
where privacy_risk_score >= 70
  and consent_requirement not in ('Required')
  and review_status not like '%review%';

-- Check 4: experiment-ready features must include a guardrail metric.
select *
from experiment_plans
where guardrail_metric is null
   or trim(guardrail_metric) = '';
""",
    )

    write_text(
        ROOT / "STATUS.md",
        """# Status

- Status: upgraded through the Portfolio Artifact Upgrade Workflow.
- Safe to link as an AI product management, PRD, roadmap, model evaluation, experimentation, and trust review portfolio artifact after changes are pushed.
""",
    )


def write_readme():
    write_text(
        ROOT / "README.md",
        """# AI Planner Feature Prioritization Studio

An interactive AI product management portfolio artifact for a multi-app mobile subscription ecosystem building a personal and entrepreneurial resource planner. The studio shows how an AI Product Manager can turn user evidence, product telemetry, model evaluation, experiment design, and trust review into a roadmap decision.

## What this project demonstrates

- AI product roadmap prioritization across productivity, documents, finance, education, wellness, security, communication, creative, and utility workflows.
- PRD-ready requirement cards that translate ambiguous AI capabilities into user problems, acceptance criteria, metrics, and validation plans.
- Model quality review for NLP, recommendation, classification, generative, and computer vision features.
- Experiment and launch readiness logic with guardrail metrics, sample plans, privacy controls, consent requirements, and human fallback paths.

## Screenshots

![Product command center](docs/images/command-center.png)

Product command center: ranks AI planner opportunities by user evidence, business value, model readiness, privacy risk, effort, and launch gate.

![PRD studio](docs/images/prd-studio.png)

PRD studio: turns research themes into requirement cards with user stories, acceptance criteria, instrumentation, and validation plans.

![Model quality lab](docs/images/model-trust-lab.png)

Model quality lab: reviews model evaluation evidence, human acceptance, error rate, fairness gap, latency, and launch decision before scale.

## Data

All data is deterministic synthetic data generated for this public portfolio artifact. It does not represent any real company, user, app, subscription, model, or operating performance.

The generator models a multi-app mobile subscription ecosystem where:

- Productivity and document workflows tend to have larger reachable audiences.
- Finance, security, and cross-app workflows carry higher privacy and consent risk.
- Generative and computer vision workflows carry higher model complexity and evaluation risk.
- Recommendation and planning workflows receive stronger near-term roadmap weight when evidence and data quality are high.
- Weekly metrics are generated with controlled variance for adoption, conversion lift, retention lift, completion, accuracy, latency, escalation, and data quality.

Run `npm run analyze` to regenerate the data and analysis outputs with the fixed random seed.

## Project structure

| Path | Purpose |
|---|---|
| `index.html` | Static app shell. |
| `src/app.js` | Interactive product decision studio powered by generated JSON. |
| `src/styles.css` | Responsive application styling. |
| `scripts/score_operating_data.py` | Deterministic synthetic data generator and scoring model. |
| `scripts/capture_screenshots.mjs` | Screenshot capture for the README. |
| `data/` | Synthetic source datasets. |
| `analysis/outputs/` | Scored roadmap, PRD, model, experiment, trust, and app payload outputs. |
| `analysis/` | Analysis plan, methodology, SQL checks, and executive findings. |

## Role connection

This artifact demonstrates the work expected from an AI Product Manager: define an AI roadmap, translate AI and ML concepts into user-facing product requirements, partner with data science and engineering on model quality, define KPIs, design experiments, and keep privacy and ethical AI controls visible before launch.

## Run locally

```bash
npm run analyze
npm start
```

Then open `http://127.0.0.1:4173`.

## Scope

This is a static public portfolio artifact with reproducible synthetic data and transparent scoring logic. It does not connect to live app analytics, subscription systems, model endpoints, experiment platforms, privacy tooling, support tickets, app stores, or production user data. It shows how an AI product manager could structure a defensible decision workflow before implementation in production systems.
""",
    )


def main():
    DATA.mkdir(exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    opportunities = opportunity_rows()
    weekly = make_weekly_metrics()
    signals = make_research_signals()
    evals = make_model_evals()
    experiments = make_experiment_plans()
    controls = make_trust_controls()
    priority, prd, model, experiment, trust, summary, payload = aggregate(
        OPPORTUNITIES, weekly, signals, evals, experiments, controls
    )

    write_csv(DATA / "ai_opportunities.csv", opportunities, list(opportunities[0].keys()))
    write_csv(DATA / "weekly_product_metrics.csv", weekly, list(weekly[0].keys()))
    write_csv(DATA / "research_signals.csv", signals, list(signals[0].keys()))
    write_csv(DATA / "model_evaluations.csv", evals, list(evals[0].keys()))
    write_csv(DATA / "experiment_plans.csv", experiments, list(experiments[0].keys()))
    write_csv(DATA / "trust_controls.csv", controls, list(controls[0].keys()))

    write_csv(OUTPUTS / "priority_queue.csv", priority, list(priority[0].keys()))
    write_csv(OUTPUTS / "prd_cards.csv", prd, list(prd[0].keys()))
    write_csv(OUTPUTS / "model_quality_queue.csv", model, list(model[0].keys()))
    write_csv(OUTPUTS / "experiment_readiness.csv", experiment, list(experiment[0].keys()))
    write_csv(OUTPUTS / "trust_review_queue.csv", trust, list(trust[0].keys()))
    write_text(OUTPUTS / "summary.json", json.dumps(summary, indent=2))
    write_text(OUTPUTS / "app_payload.json", json.dumps(payload, indent=2))

    write_docs(summary)
    write_readme()

    print(f"Generated {len(opportunities)} AI opportunities.")
    print(f"Top feature: {summary['top_feature']['feature_name']} ({summary['top_feature']['priority_score']})")
    print(f"Ready experiments: {summary['ready_experiments']}")
    print(f"Launch blockers: {summary['launch_blockers']}")


if __name__ == "__main__":
    main()
