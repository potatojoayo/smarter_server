from django.contrib import admin

from inform.models import Notice, NotificationType, PushNotification


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass

@admin.register(NotificationType)
class NotificationType(admin.ModelAdmin):
    pass

@admin.register(PushNotification)
class PushNotification(admin.ModelAdmin):
    pass
