from django.contrib import admin
from models import CompanyMonthly

# Register your models here.
class CompanyMonthlyAdmin(admin.ModelAdmin):

    list_display = ('month', 'company',  'std', 'market_value', 'book_value', 'sales', 'returns')
    list_filter = ('month', 'company', )
    search_fields = [ 'company',  'std', 'market_value', 'book_value', 'sales']
admin.site.register(CompanyMonthly, CompanyMonthlyAdmin)