from django.contrib import admin
from src.web.website.models import LocalGuide

@admin.register(LocalGuide)
class LocalGuideAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'rating', 'review_count', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('user__first_name', 'user__last_name', 'expertise')
    ordering = ('-rating', '-review_count')
