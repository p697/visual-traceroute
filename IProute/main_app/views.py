from django.shortcuts import render
from django.http import HttpResponse
from . import procs
import json


def index(request):
    return render(request, 'main_app/index.html')


def getRoute(request):
    ip = request.GET.get('ip')

    data = procs.create(ip)

    jsonData = json.dumps(data)
    # print(jsonData)
    res = HttpResponse(jsonData)
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    res['Access-Control-Max-Age'] = '1000'
    res['Access-Control-Allow-Headers'] = '*'
    return res
