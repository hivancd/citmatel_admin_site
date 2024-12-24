from django.shortcuts import render
from .models import *

def front(request):
    context={}
    return render(request,'proyects/example.html',context)
