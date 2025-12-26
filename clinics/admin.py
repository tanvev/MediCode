from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Clinic, ClinicMembership

admin.site.register(Clinic)
admin.site.register(ClinicMembership)
