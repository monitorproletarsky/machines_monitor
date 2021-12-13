# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Participant, Reason, Equipment, TimetableDetail, Timetable, TimetableContent, ClassifiedInterval
from .models import Company, Code, Profile, Workshop, Area, Repairer, Complex, Repair_reason, Repair_statistics, \
    Repairer_master_reason, Coordinator
from django.contrib import admin


class EquipmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Equipment._meta.fields]
    list_filter = ['workshop']
    search_fields = ['id', 'workshop__workshop_number', 'code', 'model']

    class Meta:
        model = Equipment


class TimetableDetailInLine(admin.TabularInline):
    model = TimetableContent


class TimetableAdmin(admin.ModelAdmin):
    inlines = [
        TimetableDetailInLine,
    ]


class ClassifiedIntervalAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']


class CodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code']


# Register your models here.
admin.site.register(Participant)
admin.site.register(Reason)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(TimetableDetail)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(ClassifiedInterval, ClassifiedIntervalAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(Workshop)
admin.site.register(Area)
admin.site.register(Repairer)
admin.site.register(Complex)
admin.site.register(Repair_reason)
admin.site.register(Repair_statistics)
admin.site.register(Repairer_master_reason)
admin.site.register(Coordinator)
admin.site.register(Company)
