from django.contrib import admin

from articles.admin import ArticleAdmin

from .models import FrequentlyAskedQuestion


admin.site.register(FrequentlyAskedQuestion, ArticleAdmin)
