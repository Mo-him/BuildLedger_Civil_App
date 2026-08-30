
from fastapi import FastAPI

from app.core.config import settings

# =========================================================
# API ROUTES
# =========================================================

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.parties import router as parties_router
from app.api.routes.projects import router as projects_router
from app.api.routes.bills import router as bills_router
from app.api.routes.payments import router as payments_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.masters import router as masters_router

from app.api.routes.bill_items import router as bill_items_router
from app.api.routes.bill_calculation import (
    router as bill_calculation_router,
)
from app.api.routes.bill_deductions import (
    router as bill_deductions_router,
)
from app.api.routes.bill_taxes import router as bill_taxes_router
from app.api.routes.bill_previous_payments import (
    router as bill_previous_payments_router,
)
from app.api.routes.bill_status_history import (
    router as bill_status_history_router,
)

from app.api.routes.company_profile import (
    router as company_profile_router,
)
from app.api.routes.user_settings import (
    router as user_settings_router,
)


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Civil Billing Management REST API",
)


# =========================================================
# API ROUTER REGISTRATION
# =========================================================

API_PREFIX = "/api"


# ---------------------------------------------------------
# Authentication & Users
# ---------------------------------------------------------

app.include_router(
    auth_router,
    prefix=API_PREFIX,
)

app.include_router(
    users_router,
    prefix=API_PREFIX,
)


# ---------------------------------------------------------
# Master Data
# ---------------------------------------------------------

app.include_router(
    masters_router,
    prefix=API_PREFIX,
)

app.include_router(
    parties_router,
    prefix=API_PREFIX,
)


# ---------------------------------------------------------
# Projects
# ---------------------------------------------------------

app.include_router(
    projects_router,
    prefix=API_PREFIX,
)


# ---------------------------------------------------------
# Billing
# ---------------------------------------------------------

app.include_router(
    bills_router,
    prefix=API_PREFIX,
)

app.include_router(
    bill_items_router,
    prefix=API_PREFIX,
)

app.include_router(
    bill_calculation_router,
    prefix=API_PREFIX,
)

app.include_router(
    bill_deductions_router,
    prefix=API_PREFIX,
)

app.include_router(
    bill_taxes_router,
    prefix=API_PREFIX,
)

app.include_router(
    bill_previous_payments_router,
    prefix=API_PREFIX,
)

app.include_router(
    bill_status_history_router,
    prefix=API_PREFIX,
)


# ---------------------------------------------------------
# Payments
# ---------------------------------------------------------

app.include_router(
    payments_router,
    prefix=API_PREFIX,
)


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

app.include_router(
    dashboard_router,
    prefix=API_PREFIX,
)


# ---------------------------------------------------------
# Company & User Settings
# ---------------------------------------------------------

app.include_router(
    company_profile_router,
    prefix=API_PREFIX,
)

app.include_router(
    user_settings_router,
    prefix=API_PREFIX,
)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get(
    "/",
    tags=["System"],
)
def root():
    return {
        "message": "Civil Billing API is running",
        "version": "1.0.0",
    }


# =========================================================
# HEALTH CHECK ENDPOINT
# =========================================================

@app.get(
    "/health",
    tags=["System"],
)
def health_check():
    return {
        "status": "healthy",
    }