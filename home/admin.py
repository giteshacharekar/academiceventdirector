from django.contrib import admin
from .models import Contact, eventlike
from .models import  Convocation
from import_export.admin import ImportExportModelAdmin

# Register your models here.d
admin.site.register((Contact, eventlike))


@admin.register(Convocation)
class ConvocationAdmin(ImportExportModelAdmin):
    pass
