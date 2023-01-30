from django.conf import settings


def global_settings(request):
    return {"ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION}

