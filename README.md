# Marketing Spend Optimization (Marketing Mix Modeling)

**Business question:** Which marketing channels actually drive sales, and how should next quarter's budget be reallocated to maximize revenue?

## Approach
1. **SQL** (`sql/queries.sql`) — aggregated 200 weeks of spend/sales data by channel, quarter, and efficiency (sales per dollar spent).
2. **Python** (`analysis.py`) — built a linear regression model estimating each channel's sales contribution per dollar spent (Marketing Mix Modeling), calculated ROI per channel, and checked for diminishing returns at high TV spend.
3. **Charts** (`charts/`) — spend-vs-sales scatter per channel, ROI comparison, diminishing-returns check.

## Key findings
- Model explains **83.4%** of week-to-week sales variance (R² on holdout weeks) — spend alone is a strong predictor of sales here
- **Baseline sales (zero marketing spend): ~$6,788/week** — this is the "organic" floor
- **ROI by channel:**
  - TV: **0.35x** — spend $1, get $0.35 in modeled sales contribution
  - Radio: **0.48x**
  - Banners: **1.19x** — the only channel returning more than it costs
- **Budget mismatch:** TV receives the largest share of spend (44.1%) despite the lowest ROI. Banners receive the smallest share (22.8%) despite the highest ROI.
- **Diminishing returns:** at the highest TV-spend quartile, average sales rise to ~$13,686/week vs ~$9,400-9,500/week in low-spend weeks — spend still helps, but the ROI math above shows it's the least efficient dollar-for-dollar.

## How to run
```
python3 analysis.py
```
Requires: pandas, scikit-learn, matplotlib

## Dataset
200 weeks of TV/Radio/Banner spend and resulting sales (Garve/datasets, public MMM teaching dataset).

## Caveats (important to say out loud in an interview)
- This is a **correlational, not causal**, model — it doesn't account for seasonality, competitor activity, or adstock/carryover effects (the idea that this week's TV ad still influences next week's sales). A production-grade MMM would model that.
- Linear regression assumes a constant return per dollar; real diminishing-returns curves are usually non-linear (log or saturation curves) — flagged as future scope below.

## Future scope
- Add adstock/carryover terms (a channel's effect decaying over several weeks, not just the week it ran)
- Model non-linear/saturating response curves instead of a flat $-per-$ coefficient
- Run an actual incrementality test (hold out a region from TV ads, compare sales) to validate the model's causal claim before reallocating real budget
