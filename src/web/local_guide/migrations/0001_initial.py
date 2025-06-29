# Generated by Django 5.2.3 on 2025-06-16 20:47

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('traveler', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('issuing_organization', models.CharField(max_length=255)),
                ('issue_date', models.DateField()),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('credential_id', models.CharField(blank=True, max_length=100, null=True)),
                ('credential_url', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LocalGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('experience_years', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='local_guide_images/')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='local_guide_cover_images/')),
                ('skills', models.TextField(blank=True, null=True)),
                ('availability', models.CharField(choices=[('AVAILABLE', 'Available'), ('UNAVAILABLE', 'Unavailable'), ('ON_VACATION', 'On Vacation')], default='AVAILABLE', max_length=20)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='local_guide_app_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Local Guide',
                'verbose_name_plural': 'Local Guides',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GuideBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_number', models.CharField(max_length=50, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('number_of_people', models.PositiveIntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('special_requests', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('traveler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_bookings', to='traveler.traveler')),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='local_guide.localguide')),
            ],
            options={
                'verbose_name': 'Guide Booking',
                'verbose_name_plural': 'Guide Bookings',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='LocalGuideCertification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_obtained', models.DateField()),
                ('certification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_guides', to='local_guide.certification')),
                ('local_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='local_guide.localguide')),
            ],
            options={
                'unique_together': {('local_guide', 'certification')},
            },
        ),
        migrations.CreateModel(
            name='LocalGuideLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proficiency', models.CharField(choices=[('BASIC', 'Basic'), ('CONVERSATIONAL', 'Conversational'), ('FLUENT', 'Fluent'), ('NATIVE', 'Native')], default='CONVERSATIONAL', max_length=20)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_guides', to='local_guide.language')),
                ('local_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages_spoken', to='local_guide.localguide')),
            ],
            options={
                'unique_together': {('local_guide', 'language')},
            },
        ),
    ]
