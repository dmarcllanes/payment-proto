import asyncpg
import polars as pl
from app.config import settings

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(settings.database_url, min_size=1, max_size=10)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def execute(query: str, *args) -> str:
    pool = await get_pool()
    return await pool.execute(query, *args)


async def fetch(query: str, *args) -> list[asyncpg.Record]:
    pool = await get_pool()
    return await pool.fetch(query, *args)


async def fetchrow(query: str, *args) -> asyncpg.Record | None:
    pool = await get_pool()
    return await pool.fetchrow(query, *args)


async def fetch_as_polars(query: str, *args) -> pl.DataFrame:
    rows = await fetch(query, *args)
    if not rows:
        return pl.DataFrame()
    return pl.DataFrame([dict(r) for r in rows])


CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS payment_attempts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     TEXT NOT NULL,
    card_last4      CHAR(4) NOT NULL,
    amount          NUMERIC(12, 2) NOT NULL,
    currency        CHAR(3) NOT NULL DEFAULT 'PHP',
    status          TEXT NOT NULL,          -- succeeded | failed | risk_blocked
    xendit_charge_id TEXT,
    failure_code    TEXT,
    ip_address      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pa_merchant_created ON payment_attempts (merchant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pa_ip_created ON payment_attempts (ip_address, created_at DESC);
"""


async def migrate() -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(CREATE_TABLES_SQL)
