# Methodology

The project uses deterministic synthetic data because public product telemetry, model evaluation data, and privacy review records do not exist for this exact product context.

The generator models a mobile subscription ecosystem with multiple app domains. Productivity and document workflows receive larger reachable audiences. Finance, security, and cross-app workflows carry higher privacy risk. Generative and computer vision workflows carry higher model complexity. Recommendation and task-planning workflows receive stronger near-term roadmap weights when user evidence and data quality are high.

The scoring model is intentionally transparent. It is not a production ML model. It is a product decision rubric that an AI product manager could explain in a roadmap review.
