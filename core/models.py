from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Mood(models.Model):
    mood = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mood


    def __str__(self):
        return f"{self.user.username} - {self.result}"
    

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    AGE_CHOICES = [
        ('<18', 'Below 18'),
        ('18-25', '18-25'),
        ('26-40', '26-40'),
        ('40+', '40+'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    CONCERN_CHOICES = [
        ('stress', 'Stress'),
        ('anxiety', 'Anxiety'),
        ('depression', 'Depression'),
        ('other', 'Other'),
    ]

    age = models.CharField(max_length=10, choices=AGE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    concern = models.CharField(max_length=20, choices=CONCERN_CHOICES)

    def __str__(self):
        return self.user.username