from __future__ import annotations

import time
import urllib.robotparser
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.services.vector_store import VectorStore


class EthicalScraper:
    def __init__(self, user_agent: str = "IRGE-Bot/1.0"):
        self.user_agent = user_agent

    def allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
            return rp.can_fetch(self.user_agent, url)
        except Exception:
            return False

    def fetch(self, url: str) -> dict:
        if not self.allowed(url):
            return {"url": url, "ok": False, "reason": "robots_disallow"}

        headers = {"User-Agent": self.user_agent}
        with httpx.Client(timeout=30, headers=headers) as client:
            resp = client.get(url)
            resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        title = soup.title.text.strip() if soup.title and soup.title.text else ""
        text = " ".join(soup.get_text(" ").split())[:5000]

        time.sleep(1.0)
        return {"url": url, "ok": True, "title": title, "text": text}


class LeadsPipeline:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.scraper = EthicalScraper()

    def enrich_from_inputs(self, inputs: list[dict]) -> list[dict]:
        enriched = []
        for item in inputs:
            enriched.append(
                {
                    **item,
                    "industry_fit_score": item.get("industry_fit_score", 0.5),
                    "next_action": item.get("next_action", "contact"),
                }
            )
        return enriched

    def scrape_and_store(self, urls: list[str]) -> list[dict]:
        results = []
        docs = []
        ids = []
        metas = []

        for idx, url in enumerate(urls):
            result = self.scraper.fetch(url)
            results.append(result)
            if result.get("ok"):
                ids.append(f"lead_doc_{idx}")
                docs.append(result["text"])
                metas.append({"source_url": url, "title": result["title"], "source_type": "scrape"})

        if docs:
            self.vector_store.upsert_leads(ids=ids, documents=docs, metadatas=metas)

        return results
