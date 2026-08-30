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
    router as bill_calculation_router
)
from app.api.routes.bill_deductions import (
    router as bill_deductions_router
)
from app.api.routes.bill_taxes import router as bill_taxes_router
from app.api.routes.bill_previous_payments import (
    router as bill_previous_payments_router
)
from app.api.routes.bill_status_history import (
    router as bill_status_history_router
)

from app.api.routes.company_profile import (
    router as company_profile_router
)
from app.api.routes.user_settings import (
    router as user_settings_router
)