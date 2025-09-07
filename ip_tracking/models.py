from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.TextField()

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"
    
class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address