from django.contrib import admin
from .models import Contact, eventlike
from .models import  Convocation
# Register your models here.
admin.site.register((Contact, eventlike))
admin.site.register((Convocation))