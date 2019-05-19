from django.contrib import admin
from .models import Department, Station, Networkstations, Organization, Net

# Register your models here.
admin.site.register([
    Department,
    Station,
    Networkstations,
    Net,
    Organization,
])
