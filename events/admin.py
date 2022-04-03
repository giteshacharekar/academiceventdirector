from django.contrib import admin 
from events.models import Post, eventComment

admin.site.register((Post, eventComment))