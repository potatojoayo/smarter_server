from django.contrib import admin

from gym_student.models.audition_detail import AuditionDetail
from gym_student.models.audition_master import AuditionMaster
from gym_student.models.parent import Parent
from gym_student.models.relationship import Relationship
from gym_student.models.school import School
from gym_student.models.student import Student


# Register your models here.

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    pass


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id","name")
    save_as = True


@admin.register(AuditionMaster)
class AuditionMasterAdmin(admin.ModelAdmin):
    pass


@admin.register(AuditionDetail)
class AuditionDetailAdmin(admin.ModelAdmin):
    pass



