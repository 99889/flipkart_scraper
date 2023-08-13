from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ScrappedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    num_reviews = models.IntegerField()
    ratings = models.FloatField()
    media_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class JWTToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
