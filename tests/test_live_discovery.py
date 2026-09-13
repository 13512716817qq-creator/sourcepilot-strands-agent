from app.live_discovery import load_live_sources, discover_live_suppliers, build_rfq


def test_live_sources_have_provenance_fields():
    records = load_live_sources()
    assert len(records) >= 6
    for r in records:
        assert r["platform"] in {"Alibaba.com", "Made-in-China.com"}
        assert r["supplier_name"]
        assert r["product_url"].startswith("https://")
        assert r["supplier_url"].startswith("https://")
        assert r["source_checked_at"]
        assert r["listed_price_min_usd"] <= r["listed_price_max_usd"]
        assert r["moq_pairs"] > 0


def test_live_discovery_prefers_quantity_fit_for_test_order():
    results = discover_live_suppliers("women's fashion shoes", requested_qty=100, limit=6)
    assert results
    assert all("live_discovery_score" in r for r in results)
    # At least one selected source must fit a 100-pair test order without forcing extra units.
    assert any(r["moq_pairs"] <= 100 for r in results)


def test_rfq_does_not_call_public_listing_a_formal_quote():
    record = discover_live_suppliers("women's fashion shoes", requested_qty=100, limit=1)[0]
    rfq = build_rfq(record, destination="Ghana", requested_qty=100)
    assert "Please quote current EXW price" in rfq
    assert "public listing price" in rfq
    assert record["supplier_name"] in rfq
