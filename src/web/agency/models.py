from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Agency(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agency'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    establish_year = models.DateField()
    cover_image = models.ImageField(upload_to='agency/cover_images/', null=True, blank=True)
    profile_image = models.ImageField(upload_to='agency/profile_images/', null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    team_size = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    logo = models.ImageField(upload_to='agency/logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name

class Branch(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='branches'
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return f"{self.name} - {self.agency.name}"

class Hotel(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='hotels'
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    price_range = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.hotel.name}"

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

class Schedule(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    departure_location = models.CharField(max_length=255)
    arrival_location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.vehicle.model} - {self.departure_location} to {self.arrival_location}"

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
    # discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    # hotels = models.ManyToManyField(Hotel, blank=True)
    vehicles = models.ManyToManyField(Vehicle, blank=True)
    places = models.ManyToManyField(Place, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.agency.name})"

   

class TourBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # Booking Details
    booking_number = models.CharField(max_length=50, unique=True)
    tour_package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    traveler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tour_bookings'
    )
    
    # Travel Details
    number_of_people = models.PositiveIntegerField(default=1)
    travel_date = models.DateField()
    special_requests = models.TextField(blank=True, null=True)
    
    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment Details
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    # Booking Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    
    # Cancellation
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tour Booking'
        verbose_name_plural = 'Tour Bookings'

    def __str__(self):
        return f"Booking #{self.booking_number} - {self.tour_package.name}"

    def save(self, *args, **kwargs):
        if not self.booking_number:
            # Generate a unique booking number
            import uuid
            self.booking_number = f"TB{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate pricing
        if self.tour_package.discount_price:
            self.price_per_person = self.tour_package.discount_price
            self.discount_amount = (self.tour_package.price - self.tour_package.discount_price) * self.number_of_people
        else:
            self.price_per_person = self.tour_package.price
            self.discount_amount = 0
        
        self.total_amount = self.tour_package.price * self.number_of_people
        self.final_amount = self.price_per_person * self.number_of_people
        
        super().save(*args, **kwargs)

    @property
    def agency(self):
        return self.tour_package.agency

    def get_traveler_profile(self):
        """Get the traveler profile if it exists"""
        try:
            return self.traveler.traveler_profile
        except:
            return None

    def can_cancel(self):
        """Check if booking can be cancelled"""
        return self.status in ['pending', 'confirmed'] and self.payment_status == 'completed'

    def cancel_booking(self, reason=""):
        """Cancel the booking"""
        if self.can_cancel():
            self.status = 'cancelled'
            self.cancellation_reason = reason
            self.cancelled_at = timezone.now()
            self.save()
            return True
        return False