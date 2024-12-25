from django.shortcuts import render
from .models import *
import json
import os

def front(request):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'choices.json'),'r') as file:
        choices_json = json.load(file)
    
    context={}
    return render(request,'proyects/example.html',context)

def example(request):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'choices.json'),'r') as file:
        choices_json = json.load(file)
    
    context={}
    return render(request,'proyects/example.html',context)