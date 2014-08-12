__author__ = 'shu'

from scipy import stats
from xlrd import open_workbook, xldate_as_tuple
import xlsxwriter
from datetime import datetime, timedelta, date
import numpy
import itertools
from itertools import groupby
from models import CompanyMonthly
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import re
from models import *
from conf import settings

def residual(real_return, intercept, gradient, market_return, date_posted, comany):
    residual_result = real_return - intercept - gradient*market_return
    this_month = date_to_month(date_posted)
    result = [this_month, comany, residual_result, ]
    return result

# excel = '/home/shu/Downloads/simple_value.xlsx'
# excel = '/home/shu/Downloads/simple_result.xlsx'
excel = '/home/shu/projects/django/finance/data/uk_data.xlsx'
# excel2 = '/home/shu/projects/django/finance/data/uk_data_result.xlsx'
# excel_result ='/home/shu/Downloads/simple_regression_result.xlsx'
# excel_result ='/home/shu/projects/django/finance/data/uk_regression_result.xlsx'

def import_data(request,):
    result = []

    dialy_rf_rm_rf()
    dialy_price_returns()

    monthly_market_value()
    monthly_book_value()
    monthly_sales()
    monthly_return()

    template = 'home.html'

    return render_to_response(template,
                              {"result": result,  },
                              context_instance=RequestContext(request))
def date_to_month(input_date):
    print type(input_date)
    if type(input_date) == float:
        seconds = (input_date - 25569) * 86400.0
        time = datetime.utcfromtimestamp(seconds)
        date = time.date()
    elif type(input_date) == str :
        date = datetime.strptime(input_date, '%d/%m/%Y').date()
    else:
        date = input_date

    month = str(date.year) + '-'+ str(date.month)
    this_month = datetime.strptime(month, '%Y-%m')
    return this_month


def date_to_date(input_date):
    if type(input_date) == float:
        seconds = (input_date - 25569) * 86400.0
        time = datetime.utcfromtimestamp(seconds)
        date = time.date()
    else:
        date = datetime.strptime(input_date, '%d/%m/%Y').date()

    return date

def dialy_rf_rm_rf():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'daily rf' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for idx, row in enumerate(range(2, sheet.nrows)):
            this_date = date_to_date(sheet.cell(row, 0).value)
            value = sheet.cell(row, 1).value

            if value and (type(value) in [float, int, long]):

                if DailyRF.objects.filter(date=this_date):
                    daily_rf = DailyRF.objects.get(date=this_date)
                else:
                    daily_rf = DailyRF()

                daily_rf.date = this_date
                daily_rf.rf = value
                daily_rf.country = settings.COUNTRY
                daily_rf.save()
    sheets_list = [i for i in sheets_names if 'daily Rm-Rf' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for idx, row in enumerate(range(3, sheet.nrows)):
            this_date = date_to_date(sheet.cell(row, 0).value)
            value = sheet.cell(row, 1).value

            if value and (type(value) in [float, int, long]):

                if DailyRF.objects.filter(date=this_date):
                    daily_rf = DailyRF.objects.get(date=this_date)
                else:
                    daily_rf = DailyRF()

                daily_rf.date = this_date
                daily_rf.rm_rf = value
                daily_rf.country = settings.COUNTRY
                daily_rf.save()

def dialy_price_returns():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'daily price' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):

            company_name = sheet.cell(0, column).value
            company_name = re.sub(" - MARKET VALUE", "", company_name,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            if Company.objects.filter(code=company_code):
                company = Company.objects.get(code=company_code)
            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_date = date_to_date(sheet.cell(row, 0).value)
                value = sheet.cell(row, column).value

                if value and (type(value) in [float, int, long]):

                    if CompanyDaily.objects.filter(company=company, date=this_date):
                        company_daily = CompanyDaily.objects.get(company=company, date=this_date)
                    else:
                        company_daily = CompanyDaily()

                    company_daily.company = company
                    company_daily.date = this_date
                    company_daily.price = value
                    if CompanyDaily.objects.filter(company=company, date=(this_date - timedelta(1))):
                        previous_price = CompanyDaily.objects.get(company=company, date=(this_date - timedelta(1))).price
                        if previous_price != 0:
                            returns = company_daily.price / previous_price - 1
                            company_daily.returns = returns
                            if DailyRF.objects.filter(date=this_date):
                                rf = DailyRF.objects.get(date=this_date).rf
                                company_daily.real_returns = returns - rf

                    company_daily.save()


def monthly_market_value():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'market value' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):

            company_name = sheet.cell(0, column).value
            company_name = re.sub(" - MARKET VALUE", "", company_name,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            if Company.objects.filter(code=company_code):
                company = Company.objects.get(code=company_code)
            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value

                if value and (type(value) in [float, int, long]):

                    if CompanyMonthly.objects.filter(company=company, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(company=company, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.month = this_month
                    company_monthly.market_value = value
                    company_monthly.save()

def monthly_book_value():

    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'book value' in i]
    
    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)
        
        for column in range(1, sheet.ncols):

            company_name = sheet.cell(0, column).value
            company_name = re.sub(" - BOOK VALUE-OUT SHARES-FISCAL", "", company_name,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            if Company.objects.filter(code=company_code):
                company = Company.objects.get(code=company_code)
            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value
                
                if value and (type(value) in [float, int, long]):
                    if CompanyMonthly.objects.filter(company=company, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(company=company, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.month = this_month
                    company_monthly.book_value = value
                    company_monthly.save()

def monthly_sales():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'sale' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):

            company_name = sheet.cell(0, column).value
            company_name = re.sub(" - SALES PER SHARE", "", company_name,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            if Company.objects.filter(code=company_code):
                company = Company.objects.get(code=company_code)
            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value

                if value and (type(value) in [float, int, long]):
                    if CompanyMonthly.objects.filter(company=company, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(company=company, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.month = this_month
                    company_monthly.sales = value
                    company_monthly.save()


def monthly_return():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'price' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):

            company_name = sheet.cell(0, column).value
            company_name = re.sub(" - SALES PER SHARE", "", company_name,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            if Company.objects.filter(code=company_code):
                company = Company.objects.get(code=company_code)
            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value

                if value and (type(value) in [float, int, long]):
                    if CompanyMonthly.objects.filter(company=company, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(company=company, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.month = this_month
                    company_monthly.returns = value
                    company_monthly.save()