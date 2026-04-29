from fasthtml.common import FastHTML, serve
from starlette.responses import JSONResponse, Response

from app.config import settings
from app.database import close_pool, migrate
from app.frontend.pages import checkout_page
from app.routes.payments import register as reg_payments
from app.routes.webhooks import register as reg_webhooks
from app.routes.admin import register as reg_admin

# ── PWA assets ──────────────────────────────────────────────────────────────

MANIFEST = {
    "name": "Jade 2D Gateway",
    "short_name": "Jade Pay",
    "description": "Secure 2D payment gateway — PCI-DSS 4.0.1 aligned",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#080c14",
    "theme_color": "#00A896",
    "orientation": "portrait-primary",
    "icons": [
        {"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
        {"src": "/icon-maskable.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "maskable"},
    ],
}

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#080c14"/>
  <rect x="16" y="16" width="480" height="480" rx="84" fill="none" stroke="#00A896" stroke-width="8" opacity="0.4"/>
  <text x="256" y="390" font-family="Arial,sans-serif" font-weight="900" font-size="340"
        text-anchor="middle" fill="#00A896">J</text>
</svg>"""

ICON_MASKABLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#00A896"/>
  <text x="256" y="390" font-family="Arial,sans-serif" font-weight="900" font-size="340"
        text-anchor="middle" fill="#080c14">J</text>
</svg>"""

SW_JS = """
const CACHE = 'jade-v1';
const SHELL = ['/', '/manifest.json', '/icon.svg'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL).catch(() => {})));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = e.request.url;
  if (url.includes('/api/') || url.includes('/webhooks/') || url.includes('xendit')) return;
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
"""

# ── App ──────────────────────────────────────────────────────────────────────

async def lifespan(app):
    if settings.database_url:
        await migrate()
    yield
    await close_pool()


app = FastHTML(lifespan=lifespan)
rt = app.route

reg_payments(rt)
reg_webhooks(rt)
reg_admin(rt)


@rt("/")
def get():
    return checkout_page(settings.xendit_public_key, simulate=settings.simulate_2d)


@rt("/health")
def get():
    return JSONResponse({"status": "ok", "service": settings.app_name})


@rt("/manifest.json")
def get():
    return JSONResponse(MANIFEST, media_type="application/manifest+json")


@rt("/sw.js")
def get():
    return Response(SW_JS, media_type="application/javascript")


@rt("/icon.svg")
def get():
    return Response(ICON_SVG, media_type="image/svg+xml")


@rt("/icon-maskable.svg")
def get():
    return Response(ICON_MASKABLE_SVG, media_type="image/svg+xml")


if __name__ == "__main__":
    serve()
