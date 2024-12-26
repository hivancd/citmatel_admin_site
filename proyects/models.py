from django.db import models 
import os,json
# Todo:
# Ability to add More choices
# Boolean filters
# Add subproject model
# Add hyperlink 

class Project(models.Model):
    
    # Add deployment links
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'choices.json'),'r') as file:
        choices_json = json.load(file)
    
    def __str__(self):
        return self.name
    
    number= models.SmallAutoField(primary_key=True,verbose_name='No.')
    name= models.CharField(max_length=20,verbose_name='Proyecto/Servicio')
    code= models.CharField(max_length=6,blank=True,null=True, unique=True, verbose_name='Código')
    service_type = models.CharField(max_length=20,choices=choices_json['service_type'],verbose_name="Tipo")
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
    
class Month(models.Model):
    
    month = models.PositiveSmallIntegerField(verbose_name='Mes',choices={1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'})
    plan = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Plan')
    real = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Real')
    
    
# class Subproject(models.Model):
    
#     # Finish
#     project = models.ForeignKey(Project,on_delete=models.CASCADE)