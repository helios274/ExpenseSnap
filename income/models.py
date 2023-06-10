from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(default=now)

    def __str__(self):
        return f"Income #{self.id} by {self.user.username}"
    
    class Meta:
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

