from django.contrib import admin

from notification.models.gym_notification import GymNotification
from notification.models.gym_notification_receiver import GymNotificationReceiver


# Register your models here.

@admin.register(GymNotification)
class GymNotificationAdmin(admin.ModelAdmin):
    pass

@admin.register(GymNotificationReceiver)
class GymNotificationReceiver(admin.ModelAdmin):
    pass
