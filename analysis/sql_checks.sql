-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.
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
