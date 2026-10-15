from django.conf import settings
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    cnpj = models.CharField(max_length=18, blank=True)
    email = models.EmailField(blank=True)
    profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    @property
    def avatar(self):
        return self.profile_picture

    def __str__(self):
        return f"Perfil de {self.user.username}"
    