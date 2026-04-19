"""Fetches the text content of a URL (typically a QR-code menu page).

Keeps things simple on purpose:
- Allow only http/https
- Cap response size to avoid hostile or accidental giant payloads
- Strip script/style tags from HTML, keep the visible text
- Preserve enough structure for the model to recognize sections

We don't ship a full HTML-to-markdown pipeline — the vision model is good enough
at parsing tag soup, and over-cleaning loses structure that the model can use.
"""
import re
from html import unescape

import httpx

from app.exceptions import PayloadTooLarge, UpstreamError

_MAX_BYTES = 2 * 1024 * 1024
_MAX_CHARS = 40_000
_DEFAULT_TIMEOUT = 15.0

_DROP_TAG_BODY = re.compile(
    r"<(script|style|noscript|template|svg)\b[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"[ \t]+")
_MULTI_NL = re.compile(r"\n{3,}")


class UrlFetcher:
    """Fetches a URL and returns plain, model-ready text."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def fetch_text(self, url: str) -> str:
        if not url or not url.lower().startswith(("http://", "https://")):
            raise UpstreamError("Only http(s) URLs are supported")

        client = self._client or httpx.AsyncClient(
            timeout=_DEFAULT_TIMEOUT, follow_redirects=True
        )
        try:
            response = await client.get(url, headers={"user-agent": "MenuAI/0.1 (+menuai.app)"})
        except httpx.HTTPError as exc:
            raise UpstreamError(f"Could not fetch {url}: {exc}") from exc
        finally:
            if self._client is None:
                await client.aclose()

        if response.status_code >= 400:
            raise UpstreamError(
                f"Upstream returned {response.status_code} for {url}"
            )

        if len(response.content) > _MAX_BYTES:
            raise PayloadTooLarge(
                f"Upstream page is {len(response.content) // 1024} KB; limit is "
                f"{_MAX_BYTES // 1024} KB"
            )

        content_type = response.headers.get("content-type", "").lower()
        if "text/" in content_type or "json" in content_type or not content_type:
            text = response.text
        else:
            raise UpstreamError(
                f"Unsupported content-type '{content_type}'. PDF and image menus aren't "
                "supported yet via URL — use the photo scan flow."
            )

        cleaned = self._html_to_text(text)
        return cleaned[:_MAX_CHARS]

    @staticmethod
    def _html_to_text(html: str) -> str:
        stripped = _DROP_TAG_BODY.sub(" ", html)
        stripped = _TAG.sub(" ", stripped)
        stripped = unescape(stripped)
        stripped = _WS.sub(" ", stripped)
        stripped = _MULTI_NL.sub("\n\n", stripped)
        return stripped.strip()


url_fetcher = UrlFetcher()
