from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def new_sale(request):
    if request.method == "POST":
        pass
    
# Create your views here.
