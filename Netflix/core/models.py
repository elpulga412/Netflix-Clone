from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from netfixFake import settings

AGE_CHOICES=(
    ('All','All'),
    ('Kids','Kids')
)

MOVIE_TYPE=(
    ('single','Single'),
    ('seasonal','Seasonal')
)



class CustomUser(AbstractUser):
    profiles=models.ManyToManyField('Profile')


class Profile(models.Model):
    name=models.CharField(max_length=225)
    age_limit=models.CharField(max_length=5,choices=AGE_CHOICES)
    uuid=models.UUIDField(default=uuid.uuid4,unique=True)


    def __str__(self):
        return self.name +" "+self.age_limit


class Movie(models.Model):
    title:str=models.CharField(max_length=225)
    description:str=models.TextField()
    created =models.DateTimeField(auto_now_add=True)
    uuid=models.UUIDField(default=uuid.uuid4,unique=True)
    type=models.CharField(max_length=10,choices=MOVIE_TYPE)
    videos=models.ManyToManyField('Video')
    flyer=models.ImageField(upload_to='images',blank=True,null=True)
    age_limit=models.CharField(max_length=5,choices=AGE_CHOICES,blank=True,null=True)
    trend = models.IntegerField(default=0)

    def __str__(self):
        return self.title


    def image_url(self):
        try:
            url = self.flyer.url
        except:
            url = ''
        return url

class Video(models.Model):
    title:str = models.CharField(max_length=225,blank=True,null=True)
    file=models.FileField(upload_to='media')

    def __str__(self):
        return self.title