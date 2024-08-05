from django.db import models

class Member(models.Model):
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    height = models.FloatField()
    medical_history = models.TextField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()

    def __str__(self):
        return self.email