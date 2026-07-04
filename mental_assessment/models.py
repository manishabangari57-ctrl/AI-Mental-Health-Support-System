from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Assessment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    q5 = models.IntegerField()

    score = models.IntegerField()
    level = models.CharField(max_length=20, default="Low")

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.level}"   # ✅ FIXED