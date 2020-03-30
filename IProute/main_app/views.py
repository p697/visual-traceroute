from django.shortcuts import render
from django.http import HttpResponse
from . import procs

def index(request):
    return render(request, 'main_app/index.html')

def getRoute(request):
    ip = request.GET.get('ip')

    state = procs.create(ip)

    if state:
        res = HttpResponse('true')
        res['Access-Control-Allow-Origin'] = '*'
        res['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS' 
        res['Access-Control-Max-Age'] = '1000'
        res['Access-Control-Allow-Headers'] = '*' 
        return res
    

