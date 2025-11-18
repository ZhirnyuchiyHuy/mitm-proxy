from django.db import models


class NetworkRule(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    host = models.CharField(max_length=255)
    path_prefix = models.CharField(max_length=255, blank=True)
    response_code= models.IntegerField(default=500)
    enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return f"{self.name}({self.path_prefix}{self.response_code})"