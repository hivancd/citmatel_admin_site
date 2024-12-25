from django.shortcuts import render
from .models import *
import json
import os

def front(request):
    fields = [field for field in Project._meta.get_fields()]
    projects =list(Project.objects.all())
    context={'fields':fields, 'projects':projects}
    return render(request,'proyects/front.html',context)

def example(request):
    
    context={}
    return render(request,'proyects/example.html',context)