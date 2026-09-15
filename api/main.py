from fastapi import FastAPI, Depends
from api.security import verify_api_key
from api.models import VerifyCarrierRequest, VerifyCarrierResponse
from api.services.carrier_verification import verify_carrier_service
from api.models import LoadSearchRequest, LoadSearchResponse
from api.services.load_search import search_loads
from api.models import NegotiationConfigRequest, NegotiationConfigResponse
from api.services.negotiation import get_negotiation_config
from api.models import CallRecordRequest, CallRecordResponse
from api.services.call_record import record_call
from api.models import MetricsSummaryResponse
from api.services.metrics import get_metrics_summary

app = FastAPI(
    title="Broker Client API",
    version="1.0.0",
    description="""
    Business operations API for an inbound carrier sales workflow.

    The service supports carrier verification, load matching, negotiation setup,
    call recording, and operational metrics aggregation for inbound sales teams.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    dependencies=[Depends(verify_api_key)],
    openapi_tags=[
        {"name": "Carrier Verification", "description": "Validate a carrier against FMCSA and assess eligibility."},
        {"name": "Load Search", "description": "Find the best available load based on lane and equipment preferences."},
        {"name": "Negotiation", "description": "Get pricing guardrails for negotiation and counter-offer workflow."},
        {"name": "Call Recording", "description": "Persist structured call outcomes and negotiation results."},
        {"name": "Metrics", "description": "Return aggregated operational metrics for recorded calls."},
    ],
)


@app.post(
    "/verify-carrier",
    response_model=VerifyCarrierResponse,
    tags=["Carrier Verification"],
    summary="Verify a carrier",
    description="Validates a carrier using the provided MC number and returns a normalized eligibility result.",
    responses={
        200: {"description": "Carrier verification was completed successfully."},
        401: {"description": "Missing or invalid API key."},
    },
)
def verify_carrier(payload: VerifyCarrierRequest):
    return verify_carrier_service(payload)


@app.post(
    "/loads/search",
    response_model=LoadSearchResponse,
    tags=["Load Search"],
    summary="Search for a matching load",
    description="Searches available loads using lane and equipment preferences and returns the best match when available.",
    responses={
        200: {"description": "Load search completed."},
        401: {"description": "Missing or invalid API key."},
    },
)
def load_search(payload: LoadSearchRequest):
    return search_loads(payload)


@app.post(
    "/negotiation/config",
    response_model=NegotiationConfigResponse,
    tags=["Negotiation"],
    summary="Get negotiation parameters",
    description="Returns the maximum rate, base rate, round limits, and counter offer rules for a specific load.",
    responses={
        200: {"description": "Negotiation configuration returned."},
        401: {"description": "Missing or invalid API key."},
    },
)
def negotiation_config(payload: NegotiationConfigRequest):
    return get_negotiation_config(payload)


@app.post(
    "/calls/record",
    response_model=CallRecordResponse,
    tags=["Call Recording"],
    summary="Record a completed call",
    description="Stores the result of a call, including outcome, sentiment, and negotiation metrics for reporting.",
    responses={
        200: {"description": "Call record created successfully."},
        401: {"description": "Missing or invalid API key."},
    },
)
def record_call_endpoint(payload: CallRecordRequest):
    return record_call(payload)


@app.get(
    "/metrics/summary",
    response_model=MetricsSummaryResponse,
    tags=["Metrics"],
    summary="Get call metrics summary",
    description="Returns aggregated call performance and negotiation metrics from recorded interactions.",
    responses={
        200: {"description": "Metrics summary generated successfully."},
        401: {"description": "Missing or invalid API key."},
    },
)
def metrics_summary():
    return get_metrics_summary()