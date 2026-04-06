from __future__ import annotations

import pandas as pd
import numpy as np

from app.services.sqlserver_repo import SQLServerRepo


class PricingETL:
    def __init__(self, repo: SQLServerRepo):
        self.repo = repo

    def extract(self, since_days: int = 90) -> pd.DataFrame:
        data = self.repo.fetch_pricing_base(since_days=since_days)
        return pd.DataFrame(data)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        df = df.copy()
        df["sale_date"] = pd.to_datetime(df["sale_date"])
        df["gross_margin"] = df["revenue"] - df["cost"]
        df["margin_pct"] = np.where(df["revenue"] > 0, df["gross_margin"] / df["revenue"], 0.0)

        agg = (
            df.groupby("product_id")
            .agg(
                avg_price=("unit_price", "mean"),
                avg_qty=("quantity", "mean"),
                total_revenue=("revenue", "sum"),
                total_cost=("cost", "sum"),
                total_units=("quantity", "sum"),
                margin_pct=("margin_pct", "mean"),
                last_sale=("sale_date", "max"),
            )
            .reset_index()
        )

        agg["days_since_last_sale"] = (
            pd.Timestamp.utcnow().tz_localize(None) - pd.to_datetime(agg["last_sale"])
        ).dt.days

        agg["demand_score"] = (
            (agg["total_units"] / agg["total_units"].max()) * 0.5
            + (1 / (1 + agg["days_since_last_sale"])) * 0.5
        )

        return agg

    def simulate_price_scenarios(
        self,
        feature_df: pd.DataFrame,
        min_margin_pct: float,
        discount_cap_pct: float = 0.15,
    ) -> list[dict]:
        scenarios = []
        if feature_df.empty:
            return scenarios

        for _, row in feature_df.iterrows():
            current = float(row["avg_price"])
            base_margin = float(row["margin_pct"])
            demand = float(row["demand_score"])

            suggested = current * (1 - min(discount_cap_pct, max(0.0, (0.08 - demand * 0.03))))
            min_allowed = current * (1 - discount_cap_pct)
            max_allowed = current * 1.10

            expected_volume_delta = (0.03 + demand * 0.10) if suggested < current else (-0.02)
            expected_margin_delta = (suggested - current) * 0.6 + (base_margin * 0.1 * current)

            scenario = {
                "product_id": str(row["product_id"]),
                "current_price": round(current, 2),
                "suggested_price": round(suggested, 2),
                "min_allowed_price": round(min_allowed, 2),
                "max_allowed_price": round(max_allowed, 2),
                "expected_margin_delta": round(expected_margin_delta, 2),
                "expected_volume_delta_pct": round(expected_volume_delta * 100, 2),
                "confidence": round(min(0.95, 0.55 + demand * 0.35), 2),
                "rationale": (
                    f"Demand={demand:.2f}, base_margin={base_margin:.2f}. "
                    f"Suggested adjustment stays inside the operating band."
                ),
                "needs_more_data": False,
            }
            scenarios.append(scenario)

        return scenarios
