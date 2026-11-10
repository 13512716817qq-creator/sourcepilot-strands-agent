"""PayPal Sandbox checkout helpers for SourcePilot.

This module intentionally targets PayPal's sandbox API only. It never sends
requests to PayPal's live production API.
"""
from __future__ import annotations

import os
from decimal import Decimal, InvalidOperation
from typing import Any

import requests

PAYPAL_SANDBOX_API = "https://api-m.sandbox.paypal.com"


class PayPalSandboxError(RuntimeError):
    """Raised when sandbox configuration or a PayPal API call fails."""


def sandbox_credentials_configured() -> bool:
    return bool(
        os.getenv("PAYPAL_CLIENT_ID", "").strip()
        and os.getenv("PAYPAL_CLIENT_SECRET", "").strip()
    )


def _credentials() -> tuple[str, str]:
    client_id = os.getenv("PAYPAL_CLIENT_ID", "").strip()
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise PayPalSandboxError(
            "PayPal Sandbox credentials are not configured. Set PAYPAL_CLIENT_ID "
            "and PAYPAL_CLIENT_SECRET in the app environment."
        )
    return client_id, client_secret


def _response_json(response: Any) -> dict[str, Any]:
    try:
        payload = response.json()
    except Exception as exc:
        raise PayPalSandboxError("PayPal returned a response that was not valid JSON.") from exc

    status_code = getattr(response, "status_code", 200)
    if status_code < 200 or status_code >= 300:
        detail = payload.get("message") or payload.get("name") or str(payload)
        raise PayPalSandboxError(f"PayPal Sandbox API error ({status_code}): {detail}")
    if not isinstance(payload, dict):
        raise PayPalSandboxError("PayPal returned an unexpected response format.")
    return payload


def _access_token(session: requests.Session) -> str:
    client_id, client_secret = _credentials()
    response = session.post(
        f"{PAYPAL_SANDBOX_API}/v1/oauth2/token",
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        timeout=20,
    )
    payload = _response_json(response)
    token = payload.get("access_token")
    if not token:
        raise PayPalSandboxError("PayPal did not return an OAuth access token.")
    return str(token)


def _format_amount(amount: str | int | float | Decimal) -> str:
    try:
        value = Decimal(str(amount)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError) as exc:
        raise PayPalSandboxError("Enter a valid payment amount.") from exc
    if not value.is_finite() or value <= 0 or value > Decimal("1000.00"):
        raise PayPalSandboxError(
            "Sandbox demo amount must be greater than 0 and no more than USD 1,000."
        )
    return f"{value:.2f}"


def create_sandbox_order(
    amount: str | int | float | Decimal,
    *,
    currency: str = "USD",
    description: str = "SourcePilot demonstration sample deposit",
    reference_id: str = "SOURCEPILOT-DEMO",
    return_url: str | None = None,
    cancel_url: str | None = None,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Create a PayPal Sandbox order and return its approval URL."""
    formatted_amount = _format_amount(amount)
    currency_code = currency.strip().upper()
    if len(currency_code) != 3 or not currency_code.isalpha():
        raise PayPalSandboxError("Currency must be a three-letter ISO currency code.")

    client = session or requests.Session()
    token = _access_token(client)
    public_url = os.getenv("SOURCEPILOT_PUBLIC_URL", "http://localhost:8501").rstrip("/")
    success_url = return_url or f"{public_url}/?paypal=return"
    failure_url = cancel_url or f"{public_url}/?paypal=cancel"

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": (reference_id or "SOURCEPILOT-DEMO")[:256],
                "description": (description or "SourcePilot demonstration payment")[:127],
                "amount": {"currency_code": currency_code, "value": formatted_amount},
            }
        ],
        "application_context": {
            "brand_name": "SourcePilot",
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "shipping_preference": "NO_SHIPPING",
            "return_url": success_url,
            "cancel_url": failure_url,
        },
    }
    response = client.post(
        f"{PAYPAL_SANDBOX_API}/v2/checkout/orders",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Prefer": "return=representation",
        },
        timeout=20,
    )
    order = _response_json(response)
    order_id = order.get("id")
    if not order_id:
        raise PayPalSandboxError("PayPal did not return an order ID.")
    approval_url = next(
        (
            link.get("href")
            for link in order.get("links", [])
            if link.get("rel") in {"approve", "payer-action"} and link.get("href")
        ),
        None,
    )
    if not approval_url:
        raise PayPalSandboxError("PayPal created an order but did not return an approval link.")
    return {
        "id": str(order_id),
        "status": order.get("status", "CREATED"),
        "approve_url": approval_url,
        "raw": order,
    }


def capture_sandbox_order(
    order_id: str,
    *,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Capture a buyer-approved PayPal Sandbox order."""
    clean_order_id = order_id.strip()
    if not clean_order_id or any(ch.isspace() for ch in clean_order_id):
        raise PayPalSandboxError("Enter a valid PayPal Sandbox order ID.")

    client = session or requests.Session()
    token = _access_token(client)
    response = client.post(
        f"{PAYPAL_SANDBOX_API}/v2/checkout/orders/{clean_order_id}/capture",
        json={},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Prefer": "return=representation",
        },
        timeout=20,
    )
    return _response_json(response)
