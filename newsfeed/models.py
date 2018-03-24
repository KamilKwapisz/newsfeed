from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Article(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    title = models.CharField(max_length=100)
    date = models.DateField()
    author = models.CharField(max_length=100)
    url = models.TextField(max_length=500)
    text = models.TextField(max_length=500)
    score = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    origin = models.CharField(max_length=30)
    is_video = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('newsfeed:index', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Source(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    name = models.CharField(max_length=20)
    url = models.TextField(max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('newsfeed:source-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + " - " + self.url

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    subscriptions = models.ManyToManyField(Source)
