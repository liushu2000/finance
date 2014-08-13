from django.contrib import admin
from models import *
from export import *

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

    list_display = ('month', 'company', 'std', 'market_value', 'book_value', 'sales', 'returns', 'book_market_value')
    list_filter = ('month',  'company', )
    search_fields = ['company',  'std', 'market_value', 'book_value', 'sales','returns', 'book_market_value']
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
    actions = [export_csv, export_xls, export_xlsx]
    list_display = ('country', 'month', 'vp')
    list_filter = ('month',  'country')
    search_fields = ['vp', 'month', ]
admin.site.register(MonthlyVP, MonthlyVPAdmin)


class MonthlySentimentAdmin(admin.ModelAdmin):
    #actions = [export_csv, export_xls, export_xlsx]
    list_display = ('country', 'month', 'sentiment',  )
    list_filter = ('country', 'month', )
    search_fields = ['sentiment', 'month', ]
admin.site.register(MonthlySentiment, MonthlySentimentAdmin)


class MonthlyGroupsAdmin(admin.ModelAdmin):
    #actions = [export_csv, export_xls, export_xlsx]
    list_display = ('country', 'month', 'group_number',  'type', 'average_returns','lastmonth_sentiment' )
    list_filter = ('country', 'type', 'lastmonth_sentiment', 'month', 'group_number', )
    search_fields = ['month', ]
admin.site.register(MonthlyGroups, MonthlyGroupsAdmin)


class MonthlyGroupsResultAdmin(admin.ModelAdmin):
    #actions = [export_csv, export_xls, export_xlsx]
    list_display = ('country', 'type', 'group_number',  'result')
    list_filter = ('country', 'type', 'group_number',)
    search_fields = ['result', ]
admin.site.register(MonthlyGroupsResult, MonthlyGroupsResultAdmin)