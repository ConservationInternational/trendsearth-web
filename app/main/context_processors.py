from datetime import datetime
from django.conf import settings


def mailto(request):
    return {
        "mailto": settings.MAIL_TO_ADMIN,
        "degraded_hex": settings.DEGRADED_HEX,
        "increasing_hex": settings.INCREASING_HEX,
        "stable_hex": settings.STABLE_HEX
    }
