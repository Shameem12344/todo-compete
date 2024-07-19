from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class User(AbstractUser):
    pass

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.completed and not self.completion_date:
            self.completion_date = timezone.now().date()
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gems = models.IntegerField(default=0)
    daily_task_limit = models.IntegerField(default=5)  # New field for task limit
    task_limit_increases = models.IntegerField(default=0)  # New field to track purchases

    def get_next_task_limit_price(self):
        base_price = 3
        return base_price + (self.task_limit_increases * 2)  # Price increases by 2 each time

    def increase_task_limit(self):
        self.daily_task_limit += 1
        self.task_limit_increases += 1
        self.save()
        
class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    effect = models.CharField(max_length=100)  # e.g., 'increase_task_limit'

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

# Signals to create a UserProfile when a new User is created

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Purchase)
def apply_purchase_effect(sender, instance, created, **kwargs):
    if created:
        if instance.item.effect == 'increase_task_limit':
            instance.user.userprofile.daily_task_limit += 1
            instance.user.userprofile.save()
