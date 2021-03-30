from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render

from .models import Certificate


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


def certificate(request: HttpRequest) -> HttpResponse:
    token = request.GET.get('token')
    if not token:
        return render(request, 'not_found.html')

    cert = Certificate.objects.filter(token=token).first()
    if not cert:
        return render(request, 'not_found.html')

    return render(request, 'certificate.html', context={
        'cert': cert,
    })
