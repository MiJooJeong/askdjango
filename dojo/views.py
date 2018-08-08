from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def mysum(request, numbers):
    # request: HttpRequest
    result = sum(map(int, numbers.split('/')))
    return HttpResponse(result)
