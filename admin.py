from django.contrib import admin
from .models import (SubAllotmentAdvice, ProvinceAllotment, CISAllotment,
                     AllotmentStatement, GAASAROMaster, ObjectCodeMaster,
                     DescriptionMaster, AdviceNumberMaster, CISMaster)



class CISInline(admin.TabularInline):
    model = CISAllotment
    extra = 1


class ProvinceInline(admin.TabularInline):
    model = ProvinceAllotment
    extra = 1


@admin.register(SubAllotmentAdvice)
class SubAllotmentAdviceAdmin(admin.ModelAdmin):
    list_display  = ['advice_number', 'date', 'region', 'to_location', 'description', 'total_amount']
    list_filter   = ['region', 'calendar_year']
    search_fields = ['advice_number', 'description', 'to_location']
    inlines       = [ProvinceInline]


@admin.register(ProvinceAllotment)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['province_name', 'province_total', 'sub_allotment']
    inlines = [CISInline]


@admin.register(CISAllotment)
class CISAdmin(admin.ModelAdmin):
    list_display = ['cis_name', 'amount', 'province_allotment']


@admin.register(AllotmentStatement)
class AllotmentStatementAdmin(admin.ModelAdmin):
    list_display  = ['project_name', 'ada_number', 'allotment_received', 'date']
    search_fields = ['project_name', 'ada_number']


@admin.register(GAASAROMaster)
class GAASAROMasterAdmin(admin.ModelAdmin):
    list_display  = ['value', 'created_at']
    search_fields = ['value']


@admin.register(ObjectCodeMaster)
class ObjectCodeMasterAdmin(admin.ModelAdmin):
    list_display  = ['value', 'created_at']
    search_fields = ['value']


@admin.register(DescriptionMaster)
class DescriptionMasterAdmin(admin.ModelAdmin):
    list_display  = ['value', 'created_at']
    search_fields = ['value']


@admin.register(AdviceNumberMaster)
class AdviceNumberMasterAdmin(admin.ModelAdmin):
    list_display  = ['value', 'created_at']
    search_fields = ['value']


@admin.register(CISMaster)
class CISMasterAdmin(admin.ModelAdmin):
    list_display  = ['province', 'cis_name', 'created_at']
    list_filter   = ['province']
    search_fields = ['province', 'cis_name']


