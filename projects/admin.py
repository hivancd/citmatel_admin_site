from django.contrib import admin
from .models import Project, Month,Subproject, Year

admin.site.register(Project)
admin.site.register(Month)
admin.site.register(Subproject)
admin.site.register(Year)