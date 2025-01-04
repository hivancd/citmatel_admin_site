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
        
        curr_year=year_objs[-1]

        if request.method == 'POST':
            curr_year= Year.objects.get(pk=int(request.POST.get('year')))

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
        for p in curr_projs_objs:
            c={}
            if 'servicio' in str(p.service_type.project_type).lower():
                service_count+=1
            else:
                project_count+=1
                
            factured_total+=p.factured_payment
            pending_total+=p.pending_payment
            
            for f in fields_name:
                
                if f == 'projectlink':
                    val=''
                    for l in p.projectlink_set.all():
                        val+=get_link_obj(l)
                    c[f]=val
                else:
                    c[f]=getattr(p,f)
                
            curr_projs.append(c)

        plan_count=Project.objects.filter(year=curr_year, in_plan=True).count()
        contrat_count=Project.objects.filter(year=curr_year, in_contrat=True).count()
        dev_count=Project.objects.filter(year=curr_year, in_dev=True).count()
        quality_count=Project.objects.filter(year=curr_year, in_quality=True).count()
        finished_count=Project.objects.filter(year=curr_year, is_finished=True).count()
        #   <td colspan="3" style="text-align: center;">Proyectos: {{project_count}}</td>  <!-- Este valor incluye todo lo que no es servicio. En el caso de Macroproyectos, que tienen-->
        #     <td colspan="2" style="text-align: center;">Servicios: {{service_count}}</td>  <!-- subproyectos, se cuentan los subproyectos-->
        #     <td></td>														                            <!-- El total Facturado la suma de todo lo que está en la columna Servicio Facturado-->	
        #     <td class="texto-pequeño">${{factured_total}}</td>                      <!-- Total facturado -->
        #     <td class="texto-pequeño">${{pending_total}}</td>                       <!-- Total pendiente por facturar --> <!-- Es la suma de todo los que está por facturar, pero si aparece un valor en rojo, no se suma. -->
        #     <td style="text-align: center;">{{plan_count}}</td>                          <!-- Total servicios en plan, se habló con cliente, no ha concretado cita inicial  --> 
        #     <td style="text-align: center;">{{contrat_count}}</td>                          <!-- Total servicios en contratación (reuniones de requisitos, oferta, firma contrato) --> 
        #     <td style="text-align: center;">{{dev_count}}</td>                          <!-- Total servicios en desarrollo --> 
        #     <td style="text-align: center;">{{quality__count}}</td>                          <!-- Total servicios en calidad -->
        #     <td style="text-align: center;">{{finished_count}}</td>
        # print(curr_projs)  
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