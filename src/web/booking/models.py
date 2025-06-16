from django.db import models
from django.conf import settings
from src.web.traveler.models import Traveler
from src.web.agency.models import Agency

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    traveler = models.ForeignKey(
        Traveler,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    trip = models.ForeignKey(
        'Trip',
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
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"Booking #{self.booking_number} - {self.traveler.full_name}"

    def save(self, *args, **kwargs):
        if not self.booking_number:
            # Generate a unique booking number
            import uuid
            self.booking_number = f"BK{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Trip(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    max_people = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to='trips/images/',
        null=True,
        blank=True
    )
    saved_by = models.ManyToManyField(
        Traveler,
        related_name='saved_trips',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'

    def __str__(self):
        return self.title 