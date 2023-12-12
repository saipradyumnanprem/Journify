from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=256, blank=True)
    lastname = models.CharField(max_length=256, blank=True)
    image = models.ImageField(default='profile_pics/default.jpg',
                              upload_to='static/profile_pics')
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        db_table = 'userprofiles'


class UserMoods(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recent_mood = models.CharField(max_length=256, blank=True)

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_moods = UserMoods.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)

    class Meta:
        db_table = 'usermoods'
