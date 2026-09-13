"""Source-backed public supplier discovery for SourcePilot.

V1 deliberately avoids brittle scraping and avoids calling public listing prices
"quotations". It uses real, publicly accessible supplier/product records captured
from Alibaba.com and Made-in-China.com, preserves the source URL, contact path,
location/address evidence, listed price range, MOQ and check date, then ranks the
records against a buyer's test-order quantity.

A future connector may use authorized marketplace APIs or a compliant search
provider to refresh records automatically. Until then every result is explicitly
labelled as a public listing snapshot and requires RFQ confirmation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "live_supplier_sources.json"


def load_live_sources() -> list[dict]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _price_mid(record: dict) -> float:
    return (float(record["listed_price_min_usd"]) + float(record["listed_price_max_usd"])) / 2


def _quantity_fit_score(moq: int, requested_qty: int) -> float:
    if moq <= requested_qty:
        return 100.0
    multiple = moq / max(requested_qty, 1)
    # Penalize quantity exposure aggressively for market-entry test orders.
    return max(0.0, 100.0 - (multiple - 1.0) * 35.0)


def _verification_score(record: dict) -> float:
    text = (record.get("verification") or "").lower()
    if "third-party" in text or "audited" in text or "verified manufacturer" in text or "sgs" in text or "bv" in text:
        return 100.0
    if "verified" in text:
        return 85.0
    return 65.0


def discover_live_suppliers(
    query: str,
    requested_qty: int = 100,
    platforms: Iterable[str] | None = None,
    limit: int = 6,
) -> list[dict]:
    """Return ranked public-source records relevant to the current sourcing query.

    V1 relevance is intentionally conservative: all seeded records are women's
    footwear records collected from the two connected public B2B sources. Query
    terms are used as a light text filter; ranking is deterministic and auditable.
    """
    records = load_live_sources()
    platform_set = {p.lower() for p in platforms} if platforms else None
    q_terms = [t.lower() for t in query.split() if len(t.strip()) >= 3]

    filtered: list[dict] = []
    for record in records:
        if platform_set and record["platform"].lower() not in platform_set:
            continue
        haystack = " ".join(
            [
                record.get("supplier_name", ""),
                record.get("product_title", ""),
                record.get("region", ""),
                record.get("platform", ""),
            ]
        ).lower()
        # Keep the seed set useful for broad sourcing phrases. If query contains
        # footwear/shoe terms, all records are eligible; otherwise require overlap.
        broad_footwear = any(term in q_terms for term in ["shoe", "shoes", "footwear", "women", "womens", "women's"])
        if not broad_footwear and q_terms and not any(term in haystack for term in q_terms):
            continue
        filtered.append(dict(record))

    if not filtered:
        return []

    price_mids = [_price_mid(r) for r in filtered]
    pmin, pmax = min(price_mids), max(price_mids)

    for record in filtered:
        mid = _price_mid(record)
        price_score = 100.0 if pmax == pmin else 100.0 - (mid - pmin) / (pmax - pmin) * 100.0
        qty_score = _quantity_fit_score(int(record["moq_pairs"]), int(requested_qty))
        verify_score = _verification_score(record)
        years = record.get("years_export")
        experience_score = min(100.0, 55.0 + (float(years) * 5.0)) if years else 60.0
        score = 0.40 * qty_score + 0.25 * price_score + 0.25 * verify_score + 0.10 * experience_score

        record["price_mid_usd"] = round(mid, 2)
        record["quantity_fit_score"] = round(qty_score, 1)
        record["source_verification_score"] = round(verify_score, 1)
        record["live_discovery_score"] = round(score, 1)
        record["requested_qty"] = requested_qty
        record["extra_units_if_moq_applies"] = max(0, int(record["moq_pairs"]) - int(requested_qty))
        record["listed_price_label"] = f"US${record['listed_price_min_usd']:.2f}–{record['listed_price_max_usd']:.2f}"

    filtered.sort(
        key=lambda r: (
            -r["live_discovery_score"],
            r["moq_pairs"],
            r["price_mid_usd"],
            r["supplier_name"],
        )
    )
    return filtered[:limit]


def build_rfq(record: dict, destination: str = "Ghana", requested_qty: int = 100, styles: str = "8–12") -> str:
    return f"""Subject: RFQ – Women's Fashion Footwear Test Order for {destination}

Hello {record['supplier_name']} team,

We are sourcing women's fashion footwear for the {destination} market and found your public listing on {record['platform']}.

Initial requirement:
- Test order target: approximately {requested_qty} pairs
- Style range: approximately {styles} designs
- Please confirm MOQ per design / color
- Please quote current EXW price in USD for the requested quantity
- Please confirm material options, size run, sample cost, customization, packaging, production lead time and payment terms
- Please confirm whether the public listing price shown on the platform is still valid for this requirement

Please also share your current catalog and the best contact person for this inquiry.

Thank you.
"""


__all__ = ["load_live_sources", "discover_live_suppliers", "build_rfq"]
