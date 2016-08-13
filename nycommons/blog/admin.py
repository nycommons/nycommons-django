from django.contrib import admin

from elephantblog.modeladmins import EntryAdmin

from .models import BlogPost


admin.site.register(BlogPost, EntryAdmin)
