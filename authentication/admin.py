from django.contrib import admin

from authentication.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'identification', 'name')
