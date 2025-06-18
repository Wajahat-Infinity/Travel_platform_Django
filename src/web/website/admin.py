from django.contrib import admin
from .models import (
    HeroSlider, PopularTour, TopActivity, BlogPost, 
    ClientLogo, NewsletterSubscriber, Testimonial, SiteSettings
)

@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'subtitle']
    ordering = ['order', '-created_at']

@admin.register(PopularTour)
class PopularTourAdmin(admin.ModelAdmin):
    list_display = ['tour_package', 'badge_type', 'is_active', 'order', 'created_at']
    list_filter = ['badge_type', 'is_active', 'created_at']
    list_editable = ['badge_type', 'is_active', 'order']
    search_fields = ['tour_package__name']
    ordering = ['order', '-created_at']

@admin.register(TopActivity)
class TopActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'description']
    ordering = ['order', '-created_at']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'post_format', 'is_published', 'published_date']
    list_filter = ['post_format', 'is_published', 'published_date']
    list_editable = ['is_published']
    search_fields = ['title', 'content', 'author_name']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_date']
    date_hierarchy = 'published_date'

@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['name']
    ordering = ['order', '-created_at']

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email']
    ordering = ['-subscribed_at']
    readonly_fields = ['subscribed_at']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'rating', 'is_active', 'order', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    list_editable = ['rating', 'is_active', 'order']
    search_fields = ['name', 'country', 'content']
    ordering = ['order', '-created_at']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'updated_at']
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of SiteSettings
        return False
