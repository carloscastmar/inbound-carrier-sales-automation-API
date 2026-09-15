# Inbound Carrier Sales Automation API

This repository contains the backend API for an inbound carrier sales automation use case built as part of a technical challenge.

The system simulates how a freight brokerage could use an AI-driven conversational platform to handle inbound carrier calls, verify carrier eligibility, match available loads, negotiate pricing, and track operational metrics.

The API represents the **client-side system** that a conversational agent would integrate with in a real-world scenario.

---

## System Overview

The solution is composed of two main parts:

1. **Conversational Layer**  
   Implemented using an AI agent. It handles inbound calls, dialog flow, negotiation, and call routing.

2. **Client API (this repository)**  
   Owns business logic, data, and reporting, including:
   - Carrier verification
   - Load search and selection
   - Negotiation constraints
   - Call outcome recording
   - Metrics aggregation

This separation mirrors a realistic freight brokerage architecture, where conversational interfaces interact with existing internal systems.

---

## Deployed API

The API is deployed using Docker and Railway and is accessible via HTTPS:

**Base URL:**  
https://inbound-carrier-sales-automation-api.onrender.com

Swagger documentation:
https://inbound-carrier-sales-automation-api.onrender.com/docs

Scalar:
https://inbound-carrier-sales-automation-api.onrender.com/scalar

---

## Authentication

All endpoints are protected using **API key authentication**.

Requests must include the following header:

X-API-Key: <your-api-key>


The API key is configured via environment variables and is not stored in source control.

---

## Available Endpoints

### Carrier Verification
**POST** `/verify-carrier`

Verifies carrier eligibility using an MC number and returns a normalized eligibility signal.

---

### Load Search
**POST** `/loads/search`

Searches available loads based on carrier-provided preferences such as origin, destination, pickup date, and equipment type.  
Returns a single best-matching load or indicates that no match was found.

---

### Negotiation Configuration
**POST** `/negotiation/config`

Returns negotiation constraints for a selected load, including starting rate, maximum rate, and allowed negotiation rounds.  
These constraints are consumed by the conversational layer to conduct rate negotiation.

---

### Call Recording
**POST** `/calls/record`

Records the outcome of an inbound call, including negotiation result, sentiment, and final disposition.  
This data serves as the source of truth for metrics and reporting.

---

### Metrics Summary
**GET** `/metrics/summary`

Returns aggregated metrics derived from recorded calls, such as:
- Booking rate
- Call outcomes
- Average negotiated rate
- Sentiment distribution

This endpoint acts as a lightweight reporting mechanism independent of platform-native analytics.

---

## Data Model

For demo purposes, data is stored using static JSON files:
- Load data simulates a brokerage’s available freight inventory.
- Call records are appended after each completed interaction.

In a production environment, these would typically be backed by a database or TMS integration.

---

## Security Considerations

- **HTTPS** is enforced at the deployment layer using managed TLS certificates.
- **API key authentication** is required for all endpoints.
- Secrets are injected via environment variables.
- Local development uses HTTP for simplicity.

Additional security measures such as rate limiting or key rotation could be introduced in a production setting depending on traffic and risk profile.

---

## Local Development

### Requirements
- Python 3.11+
- Docker (recommended)

### Build and run with Docker
```bash
docker build -t inbound-carrier-api .
docker run -p 8000:8000 \
  -e FMCSA_WEB_KEY=your_fmcsa_key \
  -e API_KEY=your_api_key \
  inbound-carrier-api
```