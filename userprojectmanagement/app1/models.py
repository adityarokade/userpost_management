from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Mst_UsrTbl(AbstractUser):
    id = models.AutoField(primary_key=True)
    UserID = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=255, null=True)
    mobile = models.BigIntegerField(null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)





class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(Mst_UsrTbl(), on_delete=models.CASCADE)
