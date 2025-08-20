# Project Title
**Stage:** Problem Framing & Scoping (Stage 01)
## Problem Statement
Oil prices are a major driver of macroeconomic volatility, influencing inflation, monetary policy, and portfolio returns. However, oil price movements are not uniform, they often shift between distinct risk regimes (e.g., high volatility, stable growth, crisis-driven shocks). Current investment processes tend to use static assumptions for oil returns and volatility, which can underestimate downside risk during regime shifts.
The problem is to systematically identify and model oil risk regimes so portfolio strategies can adapt to regime changes, improving risk-adjusted performance and downside protection.
## Stakeholder & User
Decision-maker: The Portfolio Strategy Team and Risk Committee, who decide on capital allocation and hedging overlays.
User: Quant researchers and risk managers who will apply the model outputs in portfolio simulations and monitoring dashboards.
Workflow context: The model is expected to run on a monthly cycle, updating regime classifications and risk estimates for integration into the firm’s broader asset allocation and risk overlay processes.
## Useful Answer & Decision
Type of answer: Predictive / Descriptive hybrid
Descriptive: Identify and label oil price regimes (e.g., stable, rising risk, crisis).
Predictive: Forecast near-term probability of transitioning between regimes.
Metrics: Regime classification accuracy (backtest), portfolio drawdown reduction, Sharpe ratio improvement when overlay is applied.
Artifact: A regime-detection engine that outputs:
(a) current regime label
(b) transition probabilities
(c) scenario-adjusted risk/return estimates
This artifact feeds into portfolio hedging and tactical allocation decisions.
## Assumptions & Constraints
<Bullets: data availability, capacity, latency, compliance, etc.>
## Known Unknowns / Risks
<Bullets: what’s uncertain; how you’ll test or monitor>
## Lifecycle Mapping
Goal → Stage → Deliverable
- <Goal A> → Problem Framing & Scoping (Stage 01) → <Deliverable X>
- ...
## Repo Plan
/data/, /src/, /notebooks/, /docs/ ; cadence for updates
