"""
Marketing Spend Optimization (Marketing Mix Modeling)
Business question: which channels drive sales, and how should budget be reallocated?
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ---------- 1. LOAD ----------
df = pd.read_csv("data/marketing_spend.csv", parse_dates=["Date"])
print(f"Weeks of data: {len(df)}")
print(f"Total spend: TV=${df.TV.sum():,.0f}  Radio=${df.Radio.sum():,.0f}  Banners=${df.Banners.sum():,.0f}")
print(f"Total sales: ${df.Sales.sum():,.0f}")

# ---------- 2. MODEL: how much does each channel contribute to sales? ----------
X = df[["TV", "Radio", "Banners"]]
y = df["Sales"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)
r2 = r2_score(y_test, preds)
print(f"\nModel R^2 on holdout weeks: {r2:.3f}")
print(f"Baseline sales (no marketing spend at all): ${model.intercept_:,.0f} / week")

coefs = pd.Series(model.coef_, index=["TV", "Radio", "Banners"])
print("\nSales generated per $1 spent, by channel:")
print(coefs.round(2))

# ---------- 3. ROI: total contribution vs total spend, per channel ----------
contribution = {ch: model.coef_[i] * df[ch].sum() for i, ch in enumerate(["TV", "Radio", "Banners"])}
spend_total = {ch: df[ch].sum() for ch in ["TV", "Radio", "Banners"]}
roi = {ch: contribution[ch] / spend_total[ch] if spend_total[ch] else 0 for ch in contribution}

print("\n--- Channel ROI Summary ---")
for ch in ["TV", "Radio", "Banners"]:
    print(f"{ch:8s}  total_spend=${spend_total[ch]:>10,.0f}  "
          f"est_sales_contribution=${contribution[ch]:>10,.0f}  "
          f"ROI={roi[ch]:.2f}x")

# ---------- 4. DIMINISHING RETURNS CHECK: does spend efficiency drop at high spend weeks? ----------
df["tv_bucket"] = pd.qcut(df["TV"].rank(method="first"), 4, labels=["Q1 low", "Q2", "Q3", "Q4 high"])
diminishing = df.groupby("tv_bucket", observed=True).apply(
    lambda g: pd.Series({"avg_tv_spend": g.TV.mean(), "avg_sales": g.Sales.mean()})
)
print("\nTV spend quartile vs average sales (diminishing returns check):")
print(diminishing.round(0))

# ---------- 5. CHARTS ----------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, ch in zip(axes, ["TV", "Radio", "Banners"]):
    ax.scatter(df[ch], df["Sales"], alpha=0.5, color="#1F3864")
    ax.set_xlabel(f"{ch} spend ($)")
    ax.set_ylabel("Sales ($)")
    ax.set_title(f"{ch} spend vs Sales")
plt.tight_layout()
plt.savefig("charts/spend_vs_sales.png", dpi=120)
plt.close()

plt.figure(figsize=(7, 4))
pd.Series(roi).sort_values(ascending=False).plot(kind="bar", color="#2E5F9E")
plt.ylabel("Estimated ROI (sales $ per $1 spent)")
plt.title("Channel ROI Comparison")
plt.axhline(1, color="red", linestyle="--", linewidth=1)
plt.tight_layout()
plt.savefig("charts/channel_roi.png", dpi=120)
plt.close()

plt.figure(figsize=(7, 4))
diminishing["avg_sales"].plot(kind="bar", color="#C0504D")
plt.title("Avg Sales by TV Spend Quartile (Diminishing Returns Check)")
plt.ylabel("Avg weekly sales ($)")
plt.tight_layout()
plt.savefig("charts/diminishing_returns.png", dpi=120)
plt.close()

print("\nCharts saved to charts/")
