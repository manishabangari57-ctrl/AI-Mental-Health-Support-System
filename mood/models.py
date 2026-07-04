from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Mood(models.Model):

    MOODS = [
        ('happy','Happy 😊'),
        ('neutral','Neutral 😐'),
        ('sad','Sad 😢'),
        ('angry','Angry 😡')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOODS)
    note = models.TextField(blank=True, null=True)
    sentiment = models.CharField(max_length=20, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mood
    


  