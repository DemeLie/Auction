import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=30)
    images = models.ImageField(upload_to='category_images/', blank=True, null=True)
    def __str__(self):
        return self.name

class Listing(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=3)
    images = models.ImageField(upload_to='', blank=True)
    datetime = models.DateTimeField(default=timezone.localtime())
    current_bid = models.DecimalField(max_digits=64, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return self.name
@receiver(post_delete, sender=Listing)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.images:
        if os.path.isfile(instance.images.path):
            os.remove(instance.images.path)
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    datetime = models.DateTimeField(default=timezone.localtime())
    def __str__(self):
        return self.text
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Bid(models.Model):
    bids = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='bids', on_delete=models.CASCADE)

class Notifications(models.Model):
    winner = models.ForeignKey(User, related_name='winner', on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
