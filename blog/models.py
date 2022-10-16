from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

class RecipeInstruction(models.Model):
    r_id = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    time_stamp = models.CharField(max_length=8)
    seq_no = models.IntegerField()
    instruction = models.CharField(max_length=200)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['r_id', 'seq_no'], name='r_seq'
            )
        ]