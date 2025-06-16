from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from src.web.traveler.models import Traveler

class LocalGuide(models.Model):
    AVAILABILITY_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
        ('ON_VACATION', 'On Vacation'),
    ]
    
    # Updated to use settings.AUTH_USER_MODEL instead of direct User reference
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='local_guide_app_profile'
    )
    full_name = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    image = models.ImageField(upload_to='local_guide_images/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='local_guide_cover_images/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='AVAILABLE'
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Local Guide"
        verbose_name_plural = "Local Guides"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Certification(models.Model):
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.issuing_organization})"

class LocalGuideLanguage(models.Model):
    local_guide = models.ForeignKey(
        LocalGuide,
        on_delete=models.CASCADE,
        related_name='languages_spoken'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='local_guides'
    )
    proficiency = models.CharField(
        max_length=20,
        choices=[
            ('BASIC', 'Basic'),
            ('CONVERSATIONAL', 'Conversational'),
            ('FLUENT', 'Fluent'),
            ('NATIVE', 'Native')
        ],
        default='CONVERSATIONAL'
    )
    
    class Meta:
        unique_together = ('local_guide', 'language')
    
    def __str__(self):
        return f"{self.local_guide.full_name} - {self.language.name} ({self.proficiency})"

class LocalGuideCertification(models.Model):
    local_guide = models.ForeignKey(
        LocalGuide,
        on_delete=models.CASCADE,
        related_name='certifications'
    )
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name='local_guides'
    )
    date_obtained = models.DateField()
    
    class Meta:
        unique_together = ('local_guide', 'certification')
    
    def __str__(self):
        return f"{self.local_guide.full_name} - {self.certification.name}"

class GuideBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    traveler = models.ForeignKey(
        Traveler,
        on_delete=models.CASCADE,
        related_name='guide_bookings'
    )
    guide = models.ForeignKey(
        LocalGuide,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booking_number = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_people = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Guide Booking'
        verbose_name_plural = 'Guide Bookings'

    def __str__(self):
        return f"Guide Booking #{self.booking_number} - {self.traveler.full_name}"

    def save(self, *args, **kwargs):
        if not self.booking_number:
            # Generate a unique booking number
            import uuid
            self.booking_number = f"GB{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)