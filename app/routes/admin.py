from datetime import timezone

import polars as pl
from fasthtml.common import (
    A, Body, Button, Div, Head, Html, Link,
    Main, Meta, P, Script, Span, Style, Table,
    Tbody, Td, Th, Thead, Title, Tr, H1,
)

from app.database import fetch_as_polars

STYLE = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{height:100%}

body{
  background:#060a12;color:#e2e8f0;
  font-family:'Inter',system-ui,sans-serif;
  min-height:100vh;overflow-x:hidden;
}

/* Dot grid */
body::before{
  content:'';position:fixed;inset:0;
  background-image:radial-gradient(rgba(0,168,150,0.06) 1px,transparent 1px);
  background-size:28px 28px;pointer-events:none;z-index:0;
}

/* Hero header */
.hero{
  position:relative;z-index:1;
  background:linear-gradient(135deg,rgba(0,100,90,0.4) 0%,rgba(0,40,36,0.2) 100%);
  border-bottom:1px solid rgba(0,168,150,0.15);
  padding:2rem 2rem 1.75rem;
  backdrop-filter:blur(12px);
}
.hero-inner{max-width:1200px;margin:0 auto;}
.hero-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;}
.logo-wrap{display:flex;align-items:center;gap:0.5rem;}
.logo{font-size:1.2rem;font-weight:900;color:#00BFA5;letter-spacing:0.1em;}
.logo-sub{font-size:0.72rem;color:#475569;font-weight:500;}
.back-link{display:flex;align-items:center;gap:0.4rem;font-size:0.78rem;color:#475569;text-decoration:none;transition:color 0.2s;padding:0.4rem 0.8rem;border:1px solid rgba(255,255,255,0.07);border-radius:0.5rem;}
.back-link:hover{color:#00BFA5;border-color:rgba(0,191,165,0.25);}

.hero-title{font-size:1.7rem;font-weight:800;line-height:1.2;margin-bottom:0.3rem;
  background:linear-gradient(130deg,#fff 0%,rgba(255,255,255,0.6) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:0.78rem;color:#475569;}

/* Stats */
.stats-grid{
  display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;
  max-width:1200px;margin:0 auto;
  padding:1.5rem 2rem;position:relative;z-index:1;
}
.stat-card{
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.06);
  border-radius:1rem;padding:1.1rem 1.3rem;
  position:relative;overflow:hidden;
  transition:border-color 0.2s,transform 0.2s;
  animation:stat-entry 0.5s cubic-bezier(0.34,1.1,0.64,1) both;
}
.stat-card:hover{border-color:rgba(0,191,165,0.2);transform:translateY(-2px);}
.stat-card::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(0,168,150,0.06) 0%,transparent 60%);
  pointer-events:none;
}
@keyframes stat-entry{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.stat-card:nth-child(1){animation-delay:0.05s}
.stat-card:nth-child(2){animation-delay:0.1s}
.stat-card:nth-child(3){animation-delay:0.15s}
.stat-card:nth-child(4){animation-delay:0.2s}
.stat-card:nth-child(5){animation-delay:0.25s}

.stat-icon{font-size:1.4rem;margin-bottom:0.5rem;display:block;}
.stat-label{font-size:0.65rem;text-transform:uppercase;letter-spacing:0.09em;color:#475569;font-weight:600;margin-bottom:0.3rem;}
.stat-value{font-size:1.8rem;font-weight:800;line-height:1;color:#fff;}
.stat-value.jade{color:#00BFA5;}
.stat-value.red{color:#f87171;}
.stat-value.orange{color:#fb923c;}
.stat-value.blue{color:#60a5fa;}

/* Content area */
.content{max-width:1200px;margin:0 auto;padding:0 2rem 3rem;position:relative;z-index:1;}

/* Filter bar */
.filter-bar{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:1.25rem;gap:1rem;flex-wrap:wrap;
}
.filter-tabs{display:flex;gap:0.4rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:0.75rem;padding:0.25rem;}
.filter-tab{
  padding:0.35rem 0.9rem;border-radius:0.55rem;font-size:0.75rem;font-weight:600;
  border:none;background:transparent;color:#475569;cursor:pointer;transition:all 0.2s;
  letter-spacing:0.03em;
}
.filter-tab.active{background:rgba(0,168,150,0.18);color:#00BFA5;}
.filter-tab:hover:not(.active){color:#94a3b8;background:rgba(255,255,255,0.04);}

.action-group{display:flex;gap:0.5rem;}
.refresh-btn{
  display:flex;align-items:center;gap:0.4rem;
  background:rgba(0,168,150,0.1);color:#00BFA5;
  border:1px solid rgba(0,168,150,0.22);border-radius:0.6rem;
  padding:0.4rem 0.9rem;font-size:0.75rem;font-weight:600;
  cursor:pointer;text-decoration:none;transition:all 0.2s;
}
.refresh-btn:hover{background:rgba(0,168,150,0.2);border-color:rgba(0,168,150,0.4);}

/* Table card */
.table-card{
  background:rgba(255,255,255,0.025);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:1.25rem;overflow:hidden;
}
.table-scroll{overflow-x:auto;}

table{width:100%;border-collapse:collapse;min-width:640px;}
thead{background:rgba(0,0,0,0.25);border-bottom:1px solid rgba(255,255,255,0.06);}
th{
  text-align:left;font-size:0.63rem;text-transform:uppercase;
  letter-spacing:0.09em;color:#334155;font-weight:700;
  padding:0.85rem 1.2rem;white-space:nowrap;
}
td{
  padding:0.85rem 1.2rem;font-size:0.82rem;color:#94a3b8;
  border-bottom:1px solid rgba(255,255,255,0.04);
  white-space:nowrap;transition:background 0.15s;
}
tr:last-child td{border-bottom:none;}
tbody tr{animation:row-entry 0.4s ease both;}
tbody tr:nth-child(1){animation-delay:0.05s}
tbody tr:nth-child(2){animation-delay:0.08s}
tbody tr:nth-child(3){animation-delay:0.11s}
tbody tr:nth-child(4){animation-delay:0.14s}
tbody tr:nth-child(5){animation-delay:0.17s}
@keyframes row-entry{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:translateX(0)}}
tbody tr:hover td{background:rgba(255,255,255,0.025);}

.td-amount{font-weight:700;color:#fff;font-size:0.88rem;}
.td-time{color:#475569;font-size:0.78rem;}
.td-merchant{color:#e2e8f0;font-weight:500;}
.td-ip{font-family:monospace;font-size:0.75rem;color:#334155;}
.td-charge{font-family:monospace;font-size:0.72rem;color:#334155;}
.td-failure{font-size:0.75rem;color:#ef4444;}

/* Status badges */
.badge-status{
  display:inline-flex;align-items:center;gap:0.3rem;
  border-radius:9999px;padding:0.2rem 0.65rem;
  font-size:0.68rem;font-weight:700;letter-spacing:0.04em;
}
.badge-status::before{content:'';width:5px;height:5px;border-radius:50%;}
.s-succeeded{background:rgba(0,191,165,0.12);color:#00BFA5;border:1px solid rgba(0,191,165,0.2);}
.s-succeeded::before{background:#00BFA5;box-shadow:0 0 6px #00BFA5;}
.s-failed{background:rgba(248,113,113,0.1);color:#f87171;border:1px solid rgba(248,113,113,0.2);}
.s-failed::before{background:#f87171;}
.s-risk_blocked{background:rgba(251,146,60,0.1);color:#fb923c;border:1px solid rgba(251,146,60,0.2);}
.s-risk_blocked::before{background:#fb923c;}

/* Empty state */
.empty-state{padding:4rem;text-align:center;color:#1e293b;}
.empty-icon{font-size:2.5rem;margin-bottom:1rem;display:block;opacity:0.4;}
.empty-text{font-size:0.88rem;color:#334155;}

/* Responsive */
@media(max-width:900px){
  .stats-grid{grid-template-columns:repeat(3,1fr);}
  .hide-md{display:none;}
}
@media(max-width:600px){
  .hero{padding:1.25rem;}
  .stats-grid{grid-template-columns:repeat(2,1fr);padding:1rem;}
  .content{padding:0 1rem 2rem;}
  .stats-grid{padding:1rem 1rem;}
  .stat-value{font-size:1.5rem;}
  .hide-sm{display:none;}
  .filter-tabs{display:none;}
}
"""

JS = """
// Client-side status filter
var currentFilter = 'all';
function setFilter(f) {
  currentFilter = f;
  document.querySelectorAll('.filter-tab').forEach(function(t) {
    t.classList.toggle('active', t.dataset.filter === f);
  });
  document.querySelectorAll('tbody tr').forEach(function(row) {
    var status = row.dataset.status || '';
    row.style.display = (f === 'all' || status === f) ? '' : 'none';
  });
}
"""


def _badge(status: str):
    labels = {"succeeded": "Succeeded", "failed": "Failed", "risk_blocked": "Blocked"}
    return Span(labels.get(status, status), cls=f"badge-status s-{status}")


def _fmt_time(dt) -> str:
    if dt is None:
        return "—"
    if hasattr(dt, "astimezone"):
        dt = dt.astimezone(timezone.utc)
        return dt.strftime("%b %d · %H:%M")
    return str(dt)[:16]


async def admin_page() -> Html:
    df = await fetch_as_polars(
        "SELECT * FROM payment_attempts ORDER BY created_at DESC LIMIT 200"
    )
    total = df.height
    succeeded = df.filter(pl.col("status") == "succeeded").height if total else 0
    failed    = df.filter(pl.col("status") == "failed").height if total else 0
    blocked   = df.filter(pl.col("status") == "risk_blocked").height if total else 0
    volume = 0.0
    if total:
        v = df.filter(pl.col("status") == "succeeded").select(pl.col("amount").sum())
        volume = float(v.item()) if v.height > 0 else 0.0

    if total == 0:
        rows = [Tr(Td(
            Span("💳", cls="empty-icon"),
            P("No transactions yet. Make your first payment.", cls="empty-text"),
            cls="empty-state", colspan="7",
        ))]
    else:
        rows = [
            Tr(
                Td(_fmt_time(r["created_at"]), cls="td-time"),
                Td(r["merchant_id"] or "—", cls="td-merchant"),
                Td(f"PHP {float(r['amount']):,.2f}", cls="td-amount"),
                Td(_badge(r["status"] or "—")),
                Td(r["ip_address"] or "—", cls="td-ip hide-sm"),
                Td(Span(r["xendit_charge_id"] or "—", cls="td-charge"), cls="hide-md"),
                Td(r["failure_code"] or "—", cls="td-failure hide-md"),
                data_status=r["status"] or "",
            )
            for r in df.iter_rows(named=True)
        ]

    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Title("Jade Admin — Transactions"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"),
            Link(rel="icon", href="/icon.svg", type="image/svg+xml"),
            Style(STYLE),
        ),
        Body(
            # Hero header
            Div(
                Div(
                    Div(
                        Div(
                            Span("JADE", cls="logo"),
                            Span("Admin", cls="logo-sub"),
                            cls="logo-wrap",
                        ),
                        A("← Checkout", href="/", cls="back-link"),
                        cls="hero-top",
                    ),
                    H1("Transactions", cls="hero-title"),
                    P(f"Showing last {min(total,200)} records · Neon Postgres", cls="hero-sub"),
                    cls="hero-inner",
                ),
                cls="hero",
            ),

            # Stats
            Div(
                Div(Span("📊", cls="stat-icon"), Div("Total", cls="stat-label"), Div(str(total), cls="stat-value"), cls="stat-card"),
                Div(Span("✅", cls="stat-icon"), Div("Succeeded", cls="stat-label"), Div(str(succeeded), cls="stat-value jade"), cls="stat-card"),
                Div(Span("❌", cls="stat-icon"), Div("Failed", cls="stat-label"), Div(str(failed), cls="stat-value red"), cls="stat-card"),
                Div(Span("🛡", cls="stat-icon"), Div("Blocked", cls="stat-label"), Div(str(blocked), cls="stat-value orange"), cls="stat-card"),
                Div(Span("💰", cls="stat-icon"), Div("Volume (PHP)", cls="stat-label"), Div(f"{volume:,.0f}", cls="stat-value jade"), cls="stat-card"),
                cls="stats-grid",
            ),

            # Table
            Main(
                Div(
                    # Filter bar
                    Div(
                        Div(
                            Button("All",       cls="filter-tab active", data_filter="all",          onclick="setFilter('all')"),
                            Button("Succeeded", cls="filter-tab",        data_filter="succeeded",    onclick="setFilter('succeeded')"),
                            Button("Failed",    cls="filter-tab",        data_filter="failed",       onclick="setFilter('failed')"),
                            Button("Blocked",   cls="filter-tab",        data_filter="risk_blocked", onclick="setFilter('risk_blocked')"),
                            cls="filter-tabs",
                        ),
                        Div(
                            A("↻ Refresh", href="/admin", cls="refresh-btn"),
                            cls="action-group",
                        ),
                        cls="filter-bar",
                    ),
                    # Table
                    Div(
                        Div(
                            Table(
                                Thead(Tr(
                                    Th("Time"), Th("Merchant"), Th("Amount"), Th("Status"),
                                    Th("IP", cls="hide-sm"),
                                    Th("Charge ID", cls="hide-md"),
                                    Th("Failure Code", cls="hide-md"),
                                )),
                                Tbody(*rows),
                            ),
                            cls="table-scroll",
                        ),
                        cls="table-card",
                    ),
                    cls="content",
                ),
            ),
            Script(JS),
        ),
    )


def register(rt):
    @rt("/admin")
    async def get():
        return await admin_page()
