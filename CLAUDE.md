# CLAUDE.md — Jade 2D Gateway Project

## Project Vision
A high-performance, international 2D payment orchestrator focused on "Vertical Micro" SaaS niches. Built for speed, security (PCI-DSS 4.0.1 alignment), and premium aesthetics.

## Tech Stack
- **Backend:** Python 3.12+ / FastAPI (Async-first)
- **Frontend:** FastHTML (Teal/Pastel/Glassmorphism theme)
- **Data Engine:** Polars (instead of Pandas) for high-velocity risk scoring
- **Database:** Neon (Serverless Postgres)
- **Payment Rail:** Xendit (Direct API / Optional 3DS mode)
- **Deployment:** Docker on Hugging Face or specialized VPS

## Code Style & Standards
- **Naming:** `snake_case` for variables/functions, `PascalCase` for Pydantic models.
- **Type Safety:** Strict type hinting required for all FastAPI routes and logic.
- **Async:** Use `httpx` for all external API calls (Xendit/Maya). No blocking `requests`.
- **Database:** Use raw SQL or lightweight ORM. Prioritize `Polars.read_database` for analytics.
- **Design:** Favor "Stealth Jade" palette (#00A896). Avoid common violet colors.

## Payment Flow (2D Logic)
1. **Frontend:** Tokenize card via Xendit.js (Client-side).
2. **Backend:** Receive `token_id` + `amount`.
3. **Risk Check:** Process via internal Polars-based velocity/fraud engine.
4. **Charge:** Call Xendit `credit_card_charges` with `is_3ds: false`.
5. **Security:** Never log or store raw PAN/CVV. Store only last 4 digits and `payment_id` in Neon.

## Common Commands
- **Run Dev:** `uvicorn main:app --reload`
- **Lint:** `ruff check .`
- **Migration:** (Custom Neon scripts for schema updates)
- **Docker Build:** `docker build -t jade-gateway-2d .`

## Error Handling
- Use custom FastAPI `HTTPException` with clear merchant-facing error codes.
- Log all failed 2D attempts to Neon for admin fraud analysis.