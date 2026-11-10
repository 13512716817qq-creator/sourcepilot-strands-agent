# SourcePilot PayPal AI Hackathon Build

## Purpose

This integration demonstrates a controlled checkout step inside an AI-assisted procurement workflow. SourcePilot prepares a procurement recommendation; the user explicitly chooses whether to create a PayPal Sandbox order for a demonstration sample deposit; the buyer approves the order in PayPal Sandbox; and the user captures it after approval.

## Current scope

- PayPal Orders v2 API, Sandbox environment only.
- OAuth 2.0 client-credentials authentication on the server side.
- Create an order and expose the PayPal Sandbox approval URL.
- Capture an order only after the buyer approves it.
- Amount validation: greater than zero and capped at USD 1,000 for the demo.
- Credentials are read from environment variables and are never stored in source control.
- The current procurement supplier profiles remain synthetic demo records; the sandbox payment is not a real supplier payment or commercial commitment.

## Setup

1. Create a free PayPal Developer account at https://developer.paypal.com/.
2. In Apps & Credentials, select Sandbox and create a REST API app associated with a Sandbox business account.
3. Copy its Sandbox Client ID and Secret.
4. Set PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET in the runtime environment. Optionally set SOURCEPILOT_PUBLIC_URL to the deployed app URL. Do not commit credentials.
5. Install dependencies with pip install -r requirements.txt.
6. Start SourcePilot with python run.py.
7. Run the procurement demo, reach the Procurement Ready result, and expand **PayPal Sandbox Checkout**.
8. Create a small test order, approve it with a PayPal Sandbox personal test account, return to SourcePilot, and capture the approved Sandbox order.

## Security and integrity

- This module hard-codes https://api-m.sandbox.paypal.com; it does not support the PayPal live API.
- Never paste Client Secret values into chat, issue trackers, public commits or demo videos.
- Use only Sandbox buyer and seller accounts for this hackathon demonstration.
- The sample payment is a workflow demonstration against synthetic procurement data. It is not a payment to a real supplier.
- A public marketplace listing is not a formal supplier quotation. A real order would require a current supplier quote, due diligence, buyer approval and separately agreed commercial terms.

## Submission checklist

- Configure valid Sandbox credentials in the demo environment.
- Verify order creation, approval redirect and capture end to end.
- Run pytest -q and retain the passing output.
- Record a public YouTube walkthrough under three minutes showing the procurement recommendation and successful Sandbox capture.
- Ensure the public repository contains the source, setup instructions and MIT license.
- Do not claim production payment processing, live supplier payments, paying users or commercial traction.
