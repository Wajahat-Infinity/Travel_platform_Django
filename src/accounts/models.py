from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField

"""
At the start please be careful to start migrations
--------------------------------------------------

STEP: 1 comment current_subscription [FIELD] in model [USER]
STEP: 1 py manage.py makemigrations accounts
STEP: 2 py manage.py migrate
Then do next ...

"""


class User(AbstractUser):

    USER_TYPE_CHOICES = (
        ('agency', 'agency'),
        ('local_guide', 'local_guide'),
        ('traveler', 'traveler'),
    )
    is_verified = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_agency = models.BooleanField(default=False)
    is_local_guide = models.BooleanField(default=False)
    is_traveler = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, max_length=200)
    country = models.CharField( max_length=200)
    profile_image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[250, 250], quality=75, force_format='PNG',
        help_text='size of logo must be 250*250 and format must be png image file', crop=['middle', 'center']
    )
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=50, default='buyer')
    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)


class Profile(models.Model):
    pass


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_registered")
def on_user_registration(sender, instance, created, **kwargs):
    """
    :TOPIC if user creates at any point the statistics model will be initialized
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    pass
