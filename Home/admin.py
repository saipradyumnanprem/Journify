from django.contrib import admin
from .models import UserProfile, UserMoods, ImageEntry, JournalCounter

# Register your models here.


class userProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname',
                    'phone_number', 'image')


class userMoodsAdmin(admin.ModelAdmin):
    list_display = ('user', 'recent_mood', 'secondary_mood', 'image_mood')


class imageEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'image',
                    'journal_counter', 'uploaded_at')


class journalCounterAdmin(admin.ModelAdmin):
    list_display = ('user', 'journal_entry_count')


admin.site.register(UserProfile, userProfileAdmin)
admin.site.register(UserMoods, userMoodsAdmin)
admin.site.register(ImageEntry, imageEntryAdmin)
admin.site.register(JournalCounter, journalCounterAdmin)
