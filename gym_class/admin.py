from django.contrib import admin

from gym_class.models import ClassMaster, AttendanceMaster
from gym_class.models.absent_request import AbsentRequest
from gym_class.models.attendance_detail import AttendanceDetail
from gym_class.models.class_detail import ClassDetail
from gym_class.models.level import Level


@admin.register(ClassMaster)
class ClassMasterAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(ClassDetail)
class ClassDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceDetail)
class AttendanceDetailAdmin(admin.ModelAdmin):
    save_as = True


@admin.register(AttendanceMaster)
class AttendanceMasterAdmin(admin.ModelAdmin):
    save_as = True


@admin.register(AbsentRequest)
class AbsentRequestAdmin(admin.ModelAdmin):
    pass
