# Recommendation Memo: Marketing Budget Reallocation

**To:** VP of Marketing
**Re:** Are we spending our advertising budget in the right place?

## The headline finding
Our largest marketing line item — TV, at 44% of budget — is our **least efficient channel**, returning an estimated $0.35 in sales per $1 spent. Our smallest line item — Banners, at 23% of budget — is our **most efficient channel**, returning an estimated $1.19 per $1 spent. We are structurally over-invested in the channel that works least, and under-invested in the one that works best.

## The numbers behind it
| Channel | Share of budget | Est. ROI |
|---|---|---|
| TV | 44.1% | 0.35x |
| Radio | 33.1% | 0.48x |
| Banners | 22.8% | **1.19x** |

Model confidence: this regression explains 83% of the week-to-week variation in sales, based on 200 weeks of historical spend data.

## Recommendation
Shift 15-20% of the TV budget toward Banners over the next two quarters, in stages rather than all at once. A full reallocation in one step risks two things this model can't yet rule out: (1) TV may have brand-awareness value beyond what weekly sales capture, and (2) Banners' high ROI could partly reflect it currently being under-saturated — meaning returns could fall as spend increases there too.

## What I'd want before recommending a full reallocation
1. **A holdout test:** pause TV spend in one region for 4-6 weeks and measure the sales gap, to separate correlation from causation
2. **Adstock modeling:** this version treats each week's spend as only affecting that week's sales — in reality, TV ads likely influence sales for several weeks afterward, which this model currently doesn't capture and which could understate TV's true value
3. **A saturation curve for Banners:** to check whether its high ROI holds as spend increases, or whether it's high specifically because current spend is low

## Bottom line
Directionally, the data says we're leaving money on the table by over-funding TV. I'd move cautiously and validate with a real test before committing the full budget shift — but the current allocation is worth challenging now, not next fiscal year.
