from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from src.web.agency.models import TourPackage
from src.web.local_guide.models import LocalGuide

class HeroSlider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='website/hero_sliders/')
    button_text = models.CharField(max_length=100, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Hero Slider'
        verbose_name_plural = 'Hero Sliders'

    def __str__(self):
        return self.title

class PopularTour(models.Model):
    tour_package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name='popular_tours'
    )
    badge_text = models.CharField(max_length=50, blank=True, null=True)
    badge_type = models.CharField(
        max_length=20,
        choices=[
            ('BESTSELLER', 'Bestseller'),
            ('FEATURED', 'Featured'),
            ('NEW', 'New'),
            ('DISCOUNT', 'Discount'),
        ],
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Popular Tour'
        verbose_name_plural = 'Popular Tours'

    def __str__(self):
        return f"{self.tour_package.name} - {self.badge_type}"

class TopActivity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='website/activities/')
    url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Top Activity'
        verbose_name_plural = 'Top Activities'

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='website/blog/')
    author_name = models.CharField(max_length=255)
    author_image = models.ImageField(upload_to='website/blog/authors/', blank=True, null=True)
    categories = models.CharField(max_length=255, blank=True, null=True)
    post_format = models.CharField(
        max_length=20,
        choices=[
            ('TEXT', 'Text'),
            ('VIDEO', 'Video'),
            ('AUDIO', 'Audio'),
            ('GALLERY', 'Gallery'),
        ],
        default='TEXT'
    )
    read_time = models.PositiveIntegerField(default=5)  # in minutes
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

class ClientLogo(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='website/client_logos/')
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Client Logo'
        verbose_name_plural = 'Client Logos'

    def __str__(self):
        return self.name

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    image = models.ImageField(upload_to='website/testimonials/')
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} - {self.country}"

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, default='Travel Platform')
    site_description = models.TextField(blank=True, null=True)
    hero_title = models.CharField(max_length=255, default='Are You Ready...')
    hero_subtitle = models.CharField(max_length=255, default='To explore new things?')
    explore_title = models.CharField(max_length=255, default='Explore more with us')
    explore_description = models.TextField(default='Join 2000+ locals & 1200+ contributors from 3000 cities')
    discount_title = models.CharField(max_length=255, default='Enjoy Your Holiday with 50% Discount')
    discount_description = models.TextField(default='Nemo enim ipsam voluptatem quia voluptas sit aspernatur')
    newsletter_title = models.CharField(max_length=255, default='Subscribe to Get Special Offers')
    newsletter_description = models.CharField(max_length=255, default='Newsletter Sign up')
    featured_in_title = models.CharField(max_length=255, default='We were featured in')
    
    # Contact Information
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_address = models.TextField(blank=True, null=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
