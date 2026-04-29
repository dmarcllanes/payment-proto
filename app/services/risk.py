from datetime import datetime, timedelta, timezone

import polars as pl

from app.config import settings
from app.database import fetch_as_polars
from app.models import RiskDecision


async def evaluate(merchant_id: str, ip_address: str, amount: float) -> RiskDecision:
    now = datetime.now(timezone.utc)
    window_1h = now - timedelta(hours=1)
    window_24h = now - timedelta(hours=24)

    df = await fetch_as_polars(
        """
        SELECT merchant_id, ip_address, amount, status, created_at
        FROM payment_attempts
        WHERE (merchant_id = $1 OR ip_address = $2)
          AND created_at >= $3
        """,
        merchant_id,
        ip_address,
        window_24h,
    )

    if df.is_empty():
        return RiskDecision(allowed=True)

    df = df.with_columns(pl.col("created_at").cast(pl.Datetime("us", "UTC")))
    window_1h_ts = pl.lit(window_1h.replace(tzinfo=None)).cast(pl.Datetime("us", "UTC"))

    # Velocity: attempts in last hour by this merchant
    attempts_1h = (
        df.filter(
            (pl.col("merchant_id") == merchant_id)
            & (pl.col("created_at") >= window_1h_ts)
        )
        .height
    )
    if attempts_1h >= settings.velocity_max_attempts_per_hour:
        return RiskDecision(allowed=False, reason="velocity_limit_exceeded")

    # Volume: cumulative amount in last 24h by merchant
    daily_volume = float(
        df.filter(
            (pl.col("merchant_id") == merchant_id)
            & (pl.col("status") == "succeeded")
        )
        .select(pl.col("amount").cast(pl.Float64).sum())
        .item()
        or 0.0
    )
    if daily_volume + amount > settings.velocity_max_amount_per_day:
        return RiskDecision(allowed=False, reason="daily_volume_limit_exceeded")

    # IP: more than 3 distinct merchants from same IP in 24h → suspicious
    ip_merchants = (
        df.filter(pl.col("ip_address") == ip_address)
        .select(pl.col("merchant_id").n_unique())
        .item()
        or 0
    )
    if ip_merchants > 3:
        return RiskDecision(allowed=False, reason="ip_multi_merchant_anomaly")

    return RiskDecision(allowed=True)
