from django.db import models
from djmoney.models.fields import MoneyField
import os,json
# Todo:
# Add subproject model
# Add hyperlink 

class Project(models.Model):
    
    # Add deployment links
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'choices.json'),'r') as file:
        choices_json = json.load(file)
    
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=6,blank=True,null=True, unique=True)
    service_type = models.CharField(max_length=20,choices=choices_json['service_type'])
    responsable = models.CharField(max_length=20)
    factured_payment = MoneyField(max_digits=9, decimal_places=2,default_currency='CUP',default=0.0)
    pending_payment = MoneyField(max_digits=9, decimal_places=2,default_currency='CUP',default=0.0)
    in_plan = models.BooleanField(default=False)
    in_contrat = models.BooleanField(default=False)
    in_dev = models.BooleanField(default=False)
    in_quality = models.BooleanField(default=False)
    is_finished =models.BooleanField(default=False)
    state = models.CharField(max_length=20,choices=choices_json['state'])
    annotations = models.TextField(max_length=250, blank=True)
    
# class Subproject(models.Model):
    
#     # Finish
#     project = models.ForeignKey(Project,on_delete=models.CASCADE)