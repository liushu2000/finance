from django.contrib import admin
from models import *


# class CountryAdmin(admin.ModelAdmin):
#
#     list_display = ('name', )
#     search_fields = ['name', ]
# admin.site.register(Country, CountryAdmin)


class CompanyAdmin(admin.ModelAdmin):

    list_display = ('name', 'code', 'country', 'alpha', 'beta')
    list_filter = ('name', 'code', 'country', )
    search_fields = ['name', 'code']
admin.site.register(Company, CompanyAdmin)


class CompanyMonthlyAdmin(admin.ModelAdmin):

    list_display = ('month', 'company', 'std', 'market_value', 'book_value', 'sales', 'returns')
    list_filter = ('month',  'company', )
    search_fields = ['company',  'std', 'market_value', 'book_value', 'sales']
admin.site.register(CompanyMonthly, CompanyMonthlyAdmin)


class CompanyDailyAdmin(admin.ModelAdmin):

    list_display = ('date', 'company', 'price', 'returns', 'real_returns' )
    list_filter = ('date',  'company',)
    search_fields = ['company', 'code', 'price', 'returns', 'real_returns']
admin.site.register(CompanyDaily, CompanyDailyAdmin)


class DailyRFAdmin(admin.ModelAdmin):

    list_display = ('date',  'country', 'rf', 'rm_rf' )
    list_filter = ('country', 'date',)
    search_fields = ['date', 'rf', 'rm_rf' ]
admin.site.register(DailyRF, DailyRFAdmin)


class MonthlyVPAdmin(admin.ModelAdmin):

    list_display = ('month', 'vp', 'country', )
    list_filter = ('month',  'country')
    search_fields = ['vp', 'month', ]
admin.site.register(MonthlyVP, MonthlyVPAdmin)