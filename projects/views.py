from django.shortcuts import render
from .models import *
import json
import os
import itertools

def front(request):
    fields = [Project._meta.get_field('number'),
              Project._meta.get_field('projectlink'),
              Project._meta.get_field('name'),
              Project._meta.get_field('code'),
              Project._meta.get_field('service_type'),
              Project._meta.get_field('factured_payment'),
              Project._meta.get_field('pending_payment'),
              Project._meta.get_field('in_plan'),
              Project._meta.get_field('in_contrat'),
              Project._meta.get_field('in_dev'),
              Project._meta.get_field('in_quality'),
              Project._meta.get_field('is_finished'),
              Project._meta.get_field('state'),
              Project._meta.get_field('annotations')
            ]
    fields_name=[field.name for field in fields]
    
    years=[]
    year_objs=[]
    for year in Year.objects.order_by('number'):
        years.append(year.number) 
        year_objs.append(year)
        
    context={}
    
    if Project.objects.count() > 0:
        
        if request.method == 'POST':
            curr_year= Year.objects.get(pk=int(request.POST.get('year')))
        else:
            curr_year=year_objs[-1]

        curr_projs_objs = list(Project.objects.filter(year=curr_year))
        curr_months = list(curr_year.month_set.order_by('month'))
        acc=0
        month_data=[]
        for m in curr_months:
            acc+=m.real
            month_data.append({'name':m.months[m.month],
                                'plan':m.plan,
                                'real':m.real,
                                'accumulate':acc})
        percentage=acc/curr_year.plan*100
        deploy_links=[ list(p.projectlink_set.all()) for p in curr_projs_objs]
        
        curr_projs=[]
        service_count=0
        project_count=0
        factured_total=0
        pending_total=0
        
        # Iteration for all the years projects
        for p in curr_projs_objs:
            c={}
            if 'servicio' in str(p.service_type.project_type).lower():
                service_count+=1
            else:
                project_count+=1
                
            factured_total+=p.factured_payment
            pending_total+=p.pending_payment
            
            # Forming proj dict
            for f in fields_name:
                if f == 'projectlink':
                    val=''
                    for l in p.projectlink_set.all():
                        val+=get_link_obj(l)
                    c[f]=val
                else:
                    val=getattr(p,f)
                    if not val: 
                        val=''
                    elif val is True:
                        val= 'X'
                    c[f]=val
            
            # getting subprojects from the project
            # has to be at the end of the project for
            subprojects = list(p.subproject_set.all())
            if len(subprojects)>0:
                for sp in range(len(subprojects)):
                    curr_projs.append(c)
                    c={}
                    for f in fields_name:
                        try:
                            val=getattr(subprojects[sp],f)
                            if f=='number':
                                val=str(getattr(p,f)) + '.'+str(sp+1)
                            elif not val: 
                                val=''
                            elif val is True:
                                val= 'X'
                            c[f]=val
                        except Exception:
                            c[f]=''
            curr_projs.append(c)

        plan_count=Project.objects.filter(year=curr_year, in_plan=True).count()
        contrat_count=Project.objects.filter(year=curr_year, in_contrat=True).count()
        dev_count=Project.objects.filter(year=curr_year, in_dev=True).count()
        quality_count=Project.objects.filter(year=curr_year, in_quality=True).count()
        finished_count=Project.objects.filter(year=curr_year, is_finished=True).count()
        print(curr_projs)  
        print(subprojects)
        proj_keys=list(curr_projs[0].keys())     
        # print(proj_keys) 
        # print(fields_name)
        context={'curr_year':curr_year,
                'curr_months':curr_months,'fields':fields, 
                'curr_projs':curr_projs, 'years':years,
                'month_data':month_data,
                'year_accumulate':acc,
                'percentage':percentage,
                'deploy_links':deploy_links,
                'proj_keys':proj_keys,
                'service_count':service_count,
                'project_count':project_count,
                'factured_total':factured_total,
                'pending_total':pending_total,
                'plan_count':plan_count,
                'contrat_count':contrat_count,
                'dev_count':dev_count,
                'quality_count':quality_count,
                'finished_count':finished_count
                }

    return render(request,'proyects/front.html',context)

def get_link_obj(link):
    return f'<a href="{link}" target="_blank"><i class="bi bi-globe-americas"></i></a>'
def example(request):
    context={}
    return render(request,'proyects/example.html',context)