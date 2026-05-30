const state = {
  payload: null,
  selectedFeatureId: null,
};

const numberFormat = new Intl.NumberFormat("en-US");

function cssToken(value) {
  return String(value).toLowerCase().replaceAll(" ", "-").replaceAll("/", "-");
}

function metric(label, value, helper) {
  return `
    <article class="metric">
      <span>${label}</span>
      <strong>${value}</strong>
      <em>${helper}</em>
    </article>
  `;
}

function badge(label) {
  return `<span class="badge ${cssToken(label)}">${label}</span>`;
}

function findFeature(featureId) {
  return state.payload.priorityQueue.find((item) => item.feature_id === featureId);
}

function findPrd(featureId) {
  return state.payload.prdCards.find((item) => item.feature_id === featureId);
}

function findModel(featureId) {
  return state.payload.modelQuality.find((item) => item.feature_id === featureId);
}

function findExperiment(featureId) {
  return state.payload.experimentReadiness.find((item) => item.feature_id === featureId);
}

function findTrust(featureId) {
  return state.payload.trustReview.find((item) => item.feature_id === featureId);
}

function renderHero() {
  const { summary } = state.payload;
  const top = summary.top_feature;
  document.querySelector("#metricGrid").innerHTML = [
    metric("AI bets scored", summary.feature_count, "planner capabilities"),
    metric("Ready experiments", summary.ready_experiments, "controlled beta candidates"),
    metric("Launch blockers", summary.launch_blockers, "trust gates to resolve"),
    metric("Model readiness", summary.avg_model_readiness, "average eval score"),
  ].join("");

  document.querySelector("#heroDecision").innerHTML = `
    <span>Recommended next bet</span>
    <strong>${top.feature_name}</strong>
    <p>${top.user_problem}</p>
    <div>${badge(top.roadmap_lane)}${badge(top.recommended_action)}</div>
  `;
}

function renderOpportunityList() {
  const rows = state.payload.priorityQueue;
  document.querySelector("#opportunityRows").innerHTML = rows
    .map((row) => `
      <tr>
        <td>
          <button type="button" class="link-button" data-feature="${row.feature_id}">${row.feature_name}</button>
          <small>${row.domain}, ${row.target_segment}</small>
        </td>
        <td>${badge(row.roadmap_lane)}</td>
        <td>${row.priority_score}</td>
        <td>${row.rice_score}</td>
        <td>${row.model_readiness}</td>
        <td>${row.privacy_risk_score}</td>
        <td>${row.recommended_action}</td>
      </tr>
    `)
    .join("");
}

function renderFeatureDetail(featureId) {
  state.selectedFeatureId = featureId;
  const feature = findFeature(featureId);
  const prd = findPrd(featureId);
  const model = findModel(featureId);
  const experiment = findExperiment(featureId);
  const trust = findTrust(featureId);

  document.querySelectorAll("[data-feature]").forEach((button) => {
    button.classList.toggle("selected", button.dataset.feature === featureId);
  });

  document.querySelector("#featureDetail").innerHTML = `
    <div class="detail-header">
      <span>${feature.domain}</span>
      <h3>${feature.feature_name}</h3>
      <p>${feature.user_problem}</p>
    </div>
    <div class="detail-grid">
      <div><span>Primary KPI</span><strong>${feature.primary_kpi}</strong></div>
      <div><span>AI method</span><strong>${feature.ai_method}</strong></div>
      <div><span>Owner</span><strong>${feature.owner}</strong></div>
      <div><span>Launch gate</span><strong>${feature.launch_gate}</strong></div>
    </div>
    <div class="prd-card">
      <span>PRD requirement</span>
      <h4>${prd.theme}</h4>
      <p>${prd.user_story}.</p>
      <p>${prd.acceptance_criteria}</p>
    </div>
    <div class="mini-bars">
      ${bar("Priority", feature.priority_score)}
      ${bar("Model", model.model_readiness)}
      ${bar("Human acceptance", model.human_acceptance_rate)}
      ${bar("Privacy risk", trust.privacy_risk_score, true)}
    </div>
    <div class="decision-note">
      <span>Experiment rule</span>
      <p>${experiment.decision_rule}</p>
    </div>
  `;
}

function bar(label, value, risk = false) {
  const width = Math.max(4, Math.min(100, Number(value)));
  return `
    <div class="bar-row ${risk ? "risk" : ""}">
      <div><span>${label}</span><strong>${value}</strong></div>
      <i><b style="width:${width}%"></b></i>
    </div>
  `;
}

function renderPrdStudio() {
  document.querySelector("#prdGrid").innerHTML = state.payload.prdCards
    .map((row) => `
      <article class="work-card">
        <div>${badge(row.severity)}${badge(row.prd_status)}</div>
        <h3>${row.feature_name}</h3>
        <p>${row.problem}</p>
        <dl>
          <div><dt>Theme</dt><dd>${row.theme}</dd></div>
          <div><dt>Metric</dt><dd>${row.instrumentation}</dd></div>
          <div><dt>Evidence</dt><dd>${row.evidence_source}, ${row.request_count} signals</dd></div>
        </dl>
      </article>
    `)
    .join("");
}

function renderModelRows() {
  document.querySelector("#modelRows").innerHTML = state.payload.modelQuality
    .map((row) => `
      <tr>
        <td>${row.feature_name}<small>${row.ai_method}</small></td>
        <td>${row.eval_set}</td>
        <td>${row.offline_quality_score}</td>
        <td>${row.human_acceptance_rate}%</td>
        <td>${row.error_rate}%</td>
        <td>${row.fairness_gap_pp} pp</td>
        <td>${row.p95_latency_ms} ms</td>
        <td>${badge(row.quality_decision)}</td>
      </tr>
    `)
    .join("");
}

function renderExperimentCards() {
  document.querySelector("#experimentGrid").innerHTML = state.payload.experimentReadiness
    .map((row) => `
      <article class="work-card experiment-card">
        <div>${badge(row.experiment_status)}${badge(`${row.duration_days} days`)}</div>
        <h3>${row.feature_name}</h3>
        <p>${row.hypothesis}</p>
        <dl>
          <div><dt>Primary metric</dt><dd>${row.primary_metric}</dd></div>
          <div><dt>Guardrail</dt><dd>${row.guardrail_metric}</dd></div>
          <div><dt>Sample</dt><dd>${row.sample_plan}</dd></div>
          <div><dt>MDE</dt><dd>${row.minimum_detectable_lift}</dd></div>
        </dl>
      </article>
    `)
    .join("");
}

function renderTrustReview() {
  document.querySelector("#trustRows").innerHTML = state.payload.trustReview
    .map((row) => `
      <tr>
        <td>${row.feature_name}</td>
        <td>${badge(row.data_sensitivity)}</td>
        <td>${row.consent_requirement}</td>
        <td>${row.retention_policy}</td>
        <td>${row.privacy_risk_score}</td>
        <td>${badge(row.launch_blocker === "Yes" ? "Blocked" : "Clear")}</td>
        <td>${row.review_status}</td>
      </tr>
    `)
    .join("");
}

function renderWeeklySparkline() {
  const topIds = state.payload.priorityQueue.slice(0, 5).map((row) => row.feature_id);
  const rows = topIds.map((featureId) => {
    const feature = findFeature(featureId);
    const metrics = state.payload.weeklyMetrics.filter((row) => row.feature_id === featureId);
    const points = metrics
      .map((row, index) => {
        const x = 20 + index * 48;
        const y = 142 - Number(row.ai_completion_rate);
        return `${x},${y}`;
      })
      .join(" ");
    return `
      <article class="spark-card">
        <span>${feature.domain}</span>
        <strong>${feature.feature_name}</strong>
        <svg viewBox="0 0 570 150" role="img" aria-label="${feature.feature_name} weekly completion">
          <polyline points="${points}" />
        </svg>
      </article>
    `;
  });
  document.querySelector("#sparkGrid").innerHTML = rows.join("");
}

function bindEvents() {
  document.body.addEventListener("click", (event) => {
    const button = event.target.closest("[data-feature]");
    if (button) {
      renderFeatureDetail(button.dataset.feature);
    }
  });
}

async function init() {
  const response = await fetch("analysis/outputs/app_payload.json");
  state.payload = await response.json();
  renderHero();
  renderOpportunityList();
  renderFeatureDetail(state.payload.summary.top_feature.feature_id);
  renderPrdStudio();
  renderModelRows();
  renderExperimentCards();
  renderTrustReview();
  renderWeeklySparkline();
  bindEvents();
  document.querySelector("#sourceCount").textContent = numberFormat.format(state.payload.weeklyMetrics.length);
}

init();
