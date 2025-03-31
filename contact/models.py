from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Contact(models.Model):
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100,)
    phone = models.CharField(max_length=100,)
    email = models.EmailField(max_length=255,)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=500,blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True,upload_to='picture/%Y/%m')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

