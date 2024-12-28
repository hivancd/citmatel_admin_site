from django.shortcuts import render
from .models import *
import json
import os
import itertools

def front(request):
    fields = [field for field in Project._meta.get_fields()]
    
    years=[]
    year_objs=[]
    for year in Year.objects.order_by('number'):
        years.append(year.number) 
        year_objs.append(year)
    
    curr_year=year_objs[-1]
    
    if request.method == 'POST':
        curr_year= Year.objects.get(pk=int(request.POST.get('year')))
    
    curr_months = list(curr_year.month_set.order_by('month'))
    curr_projs = list(curr_year.projects.order_by('number'))
    
    acc=0
    month_data=[]
    for m in curr_months:
        acc+=m.real
        month_data.append({'name':m.months[m.month],
                             'plan':m.plan,
                             'real':m.real,
                             'accumulate':acc})
    percentage=acc/curr_year.plan*100
    context={'curr_year':curr_year,
             'curr_months':curr_months,'fields':fields, 
             'curr_projs':curr_projs, 'years':years,
             'month_data':month_data,
             'year_accumulate':acc,
             'percentage':percentage
            }
    
    return render(request,'proyects/front.html',context)

def example(request):
    context={}
    return render(request,'proyects/example.html',context)