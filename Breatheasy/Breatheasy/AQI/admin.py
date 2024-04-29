from django.contrib import admin
from import_export.admin import  ImportExportModelAdmin
from AQI.models import StudentUser,Location
from . import models
# Register your models here.


admin.site.register(StudentUser)
admin.site.register(Location, ImportExportModelAdmin)