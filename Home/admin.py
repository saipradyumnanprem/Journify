from django.contrib import admin
from .models import UserProfile, UserMoods

# Register your models here.


class userProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname',
                    'phone_number', 'image')


class userMoodsAdmin(admin.ModelAdmin):
    list_display = ('user', 'recent_mood')


admin.site.register(UserProfile, userProfileAdmin)
admin.site.register(UserMoods, userMoodsAdmin)
