from __future__ import annotations

import pytest

from app.paypal_sandbox import (
    PAYPAL_SANDBOX_API,
    PayPalSandboxError,
    capture_sandbox_order,
    create_sandbox_order,
)


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)


def test_create_sandbox_order_returns_approval_link(monkeypatch):
    monkeypatch.setenv("PAYPAL_CLIENT_ID", "sandbox-client")
    monkeypatch.setenv("PAYPAL_CLIENT_SECRET", "sandbox-secret")
    session = FakeSession(
        [
            FakeResponse({"access_token": "token-123"}),
            FakeResponse(
                {
                    "id": "ORDER-123",
                    "status": "PAYER_ACTION_REQUIRED",
                    "links": [
                        {
                            "rel": "payer-action",
                            "href": "https://www.sandbox.paypal.com/checkoutnow?token=ORDER-123",
                        }
                    ],
                }
            ),
        ]
    )

    result = create_sandbox_order(
        10,
        description="Sample deposit",
        session=session,
        return_url="https://example.test/?paypal=return",
        cancel_url="https://example.test/?paypal=cancel",
    )

    assert result["id"] == "ORDER-123"
    assert result["approve_url"].startswith("https://www.sandbox.paypal.com/")
    assert session.calls[0][0] == f"{PAYPAL_SANDBOX_API}/v1/oauth2/token"
    order_call = session.calls[1]
    assert order_call[0] == f"{PAYPAL_SANDBOX_API}/v2/checkout/orders"
    assert order_call[1]["json"]["purchase_units"][0]["amount"]["value"] == "10.00"
    assert order_call[1]["json"]["application_context"]["return_url"].endswith("paypal=return")


def test_capture_sandbox_order(monkeypatch):
    monkeypatch.setenv("PAYPAL_CLIENT_ID", "sandbox-client")
    monkeypatch.setenv("PAYPAL_CLIENT_SECRET", "sandbox-secret")
    session = FakeSession(
        [
            FakeResponse({"access_token": "token-123"}),
            FakeResponse({"id": "ORDER-123", "status": "COMPLETED"}),
        ]
    )

    result = capture_sandbox_order("ORDER-123", session=session)

    assert result["status"] == "COMPLETED"
    assert session.calls[1][0] == f"{PAYPAL_SANDBOX_API}/v2/checkout/orders/ORDER-123/capture"


def test_rejects_invalid_amount_before_api_call(monkeypatch):
    monkeypatch.setenv("PAYPAL_CLIENT_ID", "sandbox-client")
    monkeypatch.setenv("PAYPAL_CLIENT_SECRET", "sandbox-secret")
    session = FakeSession([])

    with pytest.raises(PayPalSandboxError):
        create_sandbox_order(0, session=session)

    assert session.calls == []


def test_requires_sandbox_credentials(monkeypatch):
    monkeypatch.delenv("PAYPAL_CLIENT_ID", raising=False)
    monkeypatch.delenv("PAYPAL_CLIENT_SECRET", raising=False)

    with pytest.raises(PayPalSandboxError, match="credentials are not configured"):
        create_sandbox_order(10, session=FakeSession([]))
