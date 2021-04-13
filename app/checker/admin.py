from os import getenv

from django.contrib import admin

from .models import Certificate


admin.site.register(Certificate)

if getenv("AUTH") == "oauth2":
    from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken, IDToken

    # remove oauth provider from admin
    admin.site.unregister(AccessToken)
    admin.site.unregister(Application)
    admin.site.unregister(Grant)
    admin.site.unregister(RefreshToken)
    admin.site.unregister(IDToken)
