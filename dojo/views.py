from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def mysum(request, numbers):
    # request: HttpRequest
    # result = sum(map(int, numbers.split('/')))
    result = sum(map(lambda s:int(s or 0), numbers.split('/')))
    return HttpResponse(result)
