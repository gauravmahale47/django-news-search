from django.contrib import admin
from news_search.models import SearchHistory


@admin.register(SearchHistory)
class NameAdmin(admin.ModelAdmin):
    list_display = ["user", "keyword"]
