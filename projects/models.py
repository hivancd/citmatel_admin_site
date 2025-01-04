from django.core.exceptions import ValidationError
from django.db import models 
import os,json
from django import forms
from django.contrib import admin
# Todo:
# Add subproject model
# Add hyperlink 

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'choices.json'),'r') as file:
    choices_json = json.load(file)


    
class ProjectType(models.Model):
    
    def __str__(self):
        return self.project_type
    
    project_type=models.CharField(max_length=20,primary_key=True,verbose_name='Tipo de proyecto')
    
class Year(models.Model):
    
    def __str__(self):
        return str(self.number)
    
    number = models.PositiveIntegerField(primary_key=True,verbose_name="Año")
    plan= models.PositiveBigIntegerField(blank=True,default=1)
    

class Month(models.Model):
    
    months ={1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
    
    def __str__(self):
        return self.months[self.month] +' '+ str(self.year)
     
    month = models.PositiveSmallIntegerField(verbose_name='Mes',choices=months)
    plan = models.DecimalField(max_digits=9,decimal_places=2,default=0.0,verbose_name='Plan')
    real = models.DecimalField(max_digits=9,decimal_places=2,default=0.0,verbose_name='Real')
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    
    
class Project(models.Model):
    
    # Add deployment links
   
    def __str__(self):
        return self.name
    
    number= models.SmallAutoField(primary_key=True,verbose_name='No.')
    name= models.CharField(max_length=20,verbose_name='Proyecto/Servicio')
    code= models.CharField(max_length=6,blank=True,null=True, unique=True, verbose_name='Código')
    service_type = models.ForeignKey(ProjectType,on_delete=models.RESTRICT, verbose_name='Tipo de Proyecto')
    responsable = models.CharField(max_length=20,verbose_name="Responsable")
    factured_payment = models.DecimalField(max_digits=9, decimal_places=2,default=0.0,verbose_name="Facturado")
    pending_payment = models.DecimalField(max_digits=9, decimal_places=2,default=0.0,verbose_name="Pendiente")
    in_plan = models.BooleanField(default=False,verbose_name="Plan")
    in_contrat = models.BooleanField(default=False,verbose_name="Contratación")
    in_dev = models.BooleanField(default=False,verbose_name="En desarrollo")
    in_quality = models.BooleanField(default=False,verbose_name="Calidad")
    is_finished =models.BooleanField(default=False,verbose_name="Terminado")
    state = models.CharField(max_length=20,choices=choices_json['state'],verbose_name="Estado Proyecto")
    annotations = models.TextField(max_length=250, blank=True,verbose_name="Observaciones")
    year = models.ForeignKey(Year,on_delete=models.RESTRICT)
        
        
class Subproject(models.Model):
    
    def __str__(self):
        return self.name
    
    number= models.SmallAutoField(primary_key=True,verbose_name='No.')
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20,choices=choices_json['service_type'],verbose_name="Tipo")
    name= models.CharField(max_length=20,verbose_name='Proyecto/Servicio')
    responsable = models.CharField(max_length=20,verbose_name="Responsable")
    in_plan = models.BooleanField(default=False,verbose_name="Plan")
    in_contrat = models.BooleanField(default=False,verbose_name="Contratación")
    in_dev = models.BooleanField(default=False,verbose_name="En desarrollo")
    in_quality = models.BooleanField(default=False,verbose_name="Calidad")
    is_finished =models.BooleanField(default=False,verbose_name="Terminado")
    state = models.CharField(max_length=20,choices=choices_json['state'],verbose_name="Estado Proyecto")
    annotations = models.TextField(max_length=250, blank=True,verbose_name="Observaciones")


class ProjectLink(models.Model):
    
    def __str__(self):
        return self.project.__str__() +': '+ self.link.__str__()
    
    link= models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields= '__all__'
        
    def clean(self):
        cleaned_data= super().clean()
        
        in_plan=cleaned_data.get('in_plan')
        in_contrat=cleaned_data.get('in_contrat')
        in_dev=cleaned_data.get('in_dev')
        in_quality=cleaned_data.get('in_quality')
        is_finished=cleaned_data.get('is_finished')
        
        print(in_plan)
        print(in_contrat)
        print(in_dev)
        print(in_quality)
        print(is_finished)
        
        if in_plan and (in_contrat or  in_dev or in_quality or is_finished):
                raise forms.ValidationError(('LOGIC ERROR: Si el proyecto se encuentra en PLANIFICACION no puede estar en contratación, desarrollo, calidad o terminado.'),code='error1')
        if not(in_plan or in_contrat or in_dev or in_quality or is_finished):
            raise forms.ValidationError(('LOGIC ERROR: No se definió ningún estado para el proyecto.'),code='error2')
        if is_finished and (in_contrat or in_dev or in_quality or in_plan):
            raise forms.ValidationError(('LOGIC ERROR: Si el proyecto se encuentra terminado no puede estar en contratación, desarrollo, calidad o en planificación.'),code='error3')

        return cleaned_data
    
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form= ProjectForm
    list_display=('number','name','code','service_type','responsable','factured_payment',
                  'pending_payment','in_plan','in_contrat','in_dev','in_quality','is_finished',
                  'state','annotations','year','links')
    
    def links(self,proj):
        return proj.projectlink_set.all()
    
admin.register(Project,ProjectAdmin)
    
    # .SmallAutoField(primary_key=True,verbose_name='No.')
    # name= models.CharField(max_length=20,verbose_name='Proyecto/Servicio')
    # code= models.CharField(max_length=6,blank=True,null=True, unique=True, verbose_name='Código')
    # service_type = models.ForeignKey(ProjectType,on_delete=models.RESTRICT)
    # responsable = models.CharField(max_length=20,verbose_name="Responsable")
    # factured_payment = models.DecimalField(max_digits=9, decimal_places=2,default=0.0,verbose_name="Facturado")
    # pending_payment = models.DecimalField(max_digits=9, decimal_places=2,default=0.0,verbose_name="Pendiente")
    # in_plan = models.BooleanField(default=False,verbose_name="Plan")
    # in_contrat = models.BooleanField(default=False,verbose_name="Contratación")
    # in_dev = models.BooleanField(default=False,verbose_name="En desarrollo")
    # in_quality = models.BooleanField(default=False,verbose_name="Calidad")
    # is_finished =models.BooleanField(default=False,verbose_name="Terminado")
    # state = models.CharField(max_length=20,choices=choices_json['state'],verbose_name="Estado Proyecto")
    # annotations = models.TextField(max_length=250, blank=True,verbose_name="Observaciones")
    # year = models.ForeignKey(Year,on_delete=models.RESTRICT)