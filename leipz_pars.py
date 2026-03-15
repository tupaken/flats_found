from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode, urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.leipzig.de"
LISTING_PATH = "/leben-in-leipzig/bauen-und-wohnen/wohnen/sozialwohnung"


@dataclass(frozen=True)
class FlatListing:
    title: str
    url: str


class LeipzigParser:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; LeipzigFlatMonitor/1.0)"}
        )

    def _build_page_url(self, page: int) -> str:
        params = {
            "tx_lepurpose[filter][keyword]": "",
            "tx_lepurpose[filtered]": "1",
            "tx_lepurpose[filter][sortorder]": "asc",
            "tx_lepurpose[filter][sortby]": "sorting",
            "tx_lepurpose[filter][page]": str(page),
            "tx_lepurpose[filter][1365][]": "7385",
            "tx_lepurpose[filter][1484][]": "7665",
        }
        return f"{BASE_URL}{LISTING_PATH}?{urlencode(params)}#c374892"

    def _extract_listings(self, html: str) -> list[FlatListing]:
        soup = BeautifulSoup(html, "html.parser")
        anchors = soup.select("a.link-teaser[href]")

        listings: list[FlatListing] = []
        seen_urls: set[str] = set()

        for anchor in anchors:
            href = anchor.get("href", "").strip()
            if "/sozialwohnung/detail/projekt/" not in href:
                continue

            flat_url = urljoin(BASE_URL, href)
            if flat_url in seen_urls:
                continue

            title = " ".join(anchor.get_text(" ", strip=True).split())
            listings.append(FlatListing(title=title or flat_url, url=flat_url))
            seen_urls.add(flat_url)

        return listings

    def fetch_listings(self) -> list[FlatListing]:
        all_listings: list[FlatListing] = []
        seen_urls: set[str] = set()
        page = 1

        while True:
            response = self.session.get(self._build_page_url(page), timeout=self.timeout)
            response.raise_for_status()

            page_listings = self._extract_listings(response.text)
            if not page_listings:
                break

            new_on_page = 0
            for listing in page_listings:
                if listing.url in seen_urls:
                    continue
                all_listings.append(listing)
                seen_urls.add(listing.url)
                new_on_page += 1

            if new_on_page == 0:
                break

            page += 1

        return all_listings
