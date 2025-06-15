from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LocalGuide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='local_guide')
    bio = models.TextField()
    expertise = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='guides/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.expertise}"

    class Meta:
        ordering = ['-rating', '-review_count']
