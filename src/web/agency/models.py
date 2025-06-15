from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Agency(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agency_profile'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    establish_year = models.DateField()
    cover_image = models.ImageField(upload_to='agency/cover_images/', null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    team_size = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    logo = models.ImageField(upload_to='agency/logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name

class Hotel(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='hotels'
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    star_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.agency.name})"

class HotelImage(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='hotel/images/')
    is_featured = models.BooleanField(default=False)

class Vehicle(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='vehicle/images/', null=True, blank=True)

    class Meta:
        ordering = ['model']

    def __str__(self):
        return f"{self.model} ({self.registration_number})"

class Place(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='places'
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='place/images/')
    is_featured = models.BooleanField(default=False)

class TourPackage(models.Model):
    PACKAGE_TYPES = [
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium'),
        ('LUXURY', 'Luxury'),
    ]
    
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='tour_packages'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    hotels = models.ManyToManyField(Hotel, blank=True)
    vehicles = models.ManyToManyField(Vehicle, blank=True)
    places = models.ManyToManyField(Place, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.agency.name})"