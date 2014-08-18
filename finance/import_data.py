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
import time

# excel = '/home/shu/Downloads/simple_value.xlsx'
# excel = '/home/shu/Downloads/simple_result.xlsx'
# excel = '/home/shu/projects/django/finance/data/uk_data11.xlsx'
excel = settings.EXCEL
# sentiment_excel = '/home/shu/projects/django/finance/data/sentiment.xlsx'
# excel2 = '/home/shu/projects/django/finance/data/uk_data_result.xlsx'
# excel_result ='/home/shu/Downloads/simple_regression_result.xlsx'
# excel_result ='/home/shu/projects/django/finance/data/uk_regression_result.xlsx'


def cut(lst, n):
    return [lst[i::n] for i in xrange(n)]

def import_data(request,):
    result = []

    # dialy_rf_rm_rf()
    # dialy_price()
    # daily_returns



    # monthly_market_value()
    # monthly_book_value()
    # monthly_sales()
    # monthly_return()

    template = 'home.html'

    return render_to_response(template,
                              {"result": result,  },
                              context_instance=RequestContext(request))


def date_to_month(input_date):
    # print str(type(input_date))
    # print input_date
    if type(input_date) == float:
        seconds = (input_date - 25569) * 86400.0
        time = datetime.utcfromtimestamp(seconds)
        date = time.date()
    elif type(input_date) == str:
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
                print str(daily_rf) + 'RF Saved.'

    sheets_list = [i for i in sheets_names if 'daily Rm-Rf' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for idx, row in enumerate(range(3, sheet.nrows)):
            this_date = date_to_date(sheet.cell(row, 0).value)
            value = sheet.cell(row, 1).value

            if value and (type(value) in [float, int, long]) and value != 0 :

                if DailyRF.objects.filter(date=this_date):
                    daily_rf = DailyRF.objects.get(date=this_date)
                else:
                    daily_rf = DailyRF()

                daily_rf.date = this_date
                daily_rf.rm_rf = value
                daily_rf.country = settings.COUNTRY
                daily_rf.save()
                print str(daily_rf) + 'Rm-Rf Saved.'


def dialy_price_returns():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'daily price' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):
        # for column in range(1, 25):
        # for column in range(25, 50):
        # for column in range(50, 75):
        # for column in range(75, 100):
        # for column in range(100, 125):
        # for column in range(125, 150):
        # for column in range(150, 175):
        # for column in range(175, 200):
        # for column in range(200,  sheet.ncols):
        # for column in range(225, 250):
        # for column in range(250, 275):
        # for column in range(275, 300):
        # for column in range(300, 400):
        # for column in range(325, 350):
        # for column in range(350, 375):
        # for column in range(375, 400):
        # for column in range(400, 425):
        # for column in range(425, 450):
        # for column in range(450, 475):
        # for column in range(475, sheet.ncols):
        # for column in range(1, sheet.ncols):
            time_start = time.time()
            broken = 0
            company_name = sheet.cell(0, column).value
            company_name = re.sub(" - MARKET VALUE", "", company_name,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            if Company.objects.filter(code=company_code, country=settings.COUNTRY):
                company = Company.objects.get(code=company_code, country=settings.COUNTRY)
                if CompanyDaily.objects.filter(company=company, date=datetime.strptime('2012-12-31', '%Y-%m-%d')):
                    continue
                if CompanyDaily.objects.filter(company=company,):
                    last_break_point = CompanyDaily.objects.filter(company=company,).order_by('date').exclude(price=None)[0]
                    last_break_date = last_break_point.date
                    last_break_value = last_break_point.price
                    broken = 1
                    # print last_break_date
                    # print '====================================='
                    # break
                    # print CompanyDaily.objects.filter(company=company,).order_by('-date')[0].company
                    # print last_break_date



            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            l = []
            for idx, row in enumerate(range(2, sheet.nrows)):
                this_date = date_to_date(sheet.cell(row, 0).value)
                value = sheet.cell(row, column).value
                if value and (type(value) in [float, int, long]):
                    l.append([this_date, value])

            if l:
                # print l
                # if the import stopped in the middle of complet 1 company, resume
                if broken == 1:
                    l = filter(lambda x: x[0] > last_break_date, l)

                for this_date, value in l:
                    if CompanyDaily.objects.filter(company=company, date=this_date):
                        # continue
                        company_daily = CompanyDaily.objects.get(company=company, date=this_date)
                    else:
                        company_daily = CompanyDaily()

                    company_daily.company = company
                    company_daily.date = this_date
                    company_daily.price = value
                    if CompanyDaily.objects.filter(company=company, date=(this_date - timedelta(1))):
                        previous_prices = CompanyDaily.objects.filter(company=company, date=(this_date - timedelta(1)))
                        if len(previous_prices) > 1:
                            for p in previous_prices[1:]:
                                p.delete()
                        previous_price = CompanyDaily.objects.get(company=company, date=(this_date - timedelta(1))).price
                        if previous_price != 0:
                            returns = company_daily.price / previous_price - 1
                            company_daily.returns = returns
                            if DailyRF.objects.filter(date=this_date).exclude(rf=None):
                                rf = DailyRF.objects.get(date=this_date).rf
                                company_daily.real_returns = returns - rf

                    company_daily.save()
                    time_spend = time.time() - time_start
                    print 'CompanyDaily %s -- price: %s Saved. (%s)' % (str(company_daily), str(value),  time_spend)
            print 'Company %s -- price --returns-- Saved.' % str(company_name)


def clean_daily_duplicate():
    unique_fields = ['date', 'company']
    duplicates = (CompanyDaily.objects.values(*unique_fields).order_by().annotate(max_id=models.Max('id'),
                                                count_id=models.Count('id')).filter(count_id__gt=1))

    for duplicate in duplicates:
        CompanyDaily.objects.filter(**{x: duplicate[x] for x in unique_fields}).exclude(id=duplicate['max_id']).delete()
        print 'Duplicate CompanyDaily deleted.'


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
            if Company.objects.filter(code=company_code, country=settings.COUNTRY):
                company = Company.objects.get(code=company_code, country=settings.COUNTRY)
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
                    print 'CompanyMonthly %s -- Market Value %s Saved.' % (str(company_monthly), str(value))


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
            if Company.objects.filter(code=company_code, country=settings.COUNTRY):
                company = Company.objects.get(code=company_code, country=settings.COUNTRY)
            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value
                
                if value and value and (type(value) in [float, int, long]):
                    if CompanyMonthly.objects.filter(company=company, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(company=company, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.month = this_month
                    company_monthly.book_value = value
                    company_monthly.save()
                    print 'CompanyMonthly %s -- Book Value %s Saved.' % (str(company_monthly), str(value))


def monthly_book_market_value():
    for company_monthly in CompanyMonthly.objects.filter(company__country=settings.COUNTRY).exclude(book_value=None).exclude(market_value=None):

        company_monthly.book_market_value = company_monthly.book_value / company_monthly.market_value
        company_monthly.save()
        print 'CompanyMonthly %s -- Book / Market Value %s Saved.' % (str(company_monthly), str(company_monthly.book_market_value))


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
            if Company.objects.filter(code=company_code, country=settings.COUNTRY):
                company = Company.objects.get(code=company_code, country=settings.COUNTRY)
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
                    print 'CompanyMonthly %s -- Sales %s Saved.' % (str(company_monthly), str(value))


def monthly_return():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'monthly price' == i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):

            company_name = sheet.cell(0, column).value
            company_name = re.sub(" - SALES PER SHARE", "", company_name,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            if Company.objects.filter(code=company_code, country=settings.COUNTRY):
                company = Company.objects.get(code=company_code, country=settings.COUNTRY)
            else:
                company = Company()
                company.code = company_code
                company.name = company_name
                company.country = settings.COUNTRY
                company.save()

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                price = sheet.cell(row, column).value
                price_previous = sheet.cell(row-1, column).value
                if price and price_previous and (type(price_previous) in [float, int, long]) and (type(price_previous) in [float, int, long]):
                    returns = (price / price_previous) - 1
                    if CompanyMonthly.objects.filter(company=company, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(company=company, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.month = this_month
                    company_monthly.returns = returns
                    company_monthly.save()
                    print 'CompanyMonthly %s -- Returns %s Saved.' % (str(company_monthly), str(returns))


def monthly_sentiment():
    data = open_workbook(settings.SENTIMENT_EXCEL, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if settings.COUNTRY in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for idx, row in enumerate(range(1, sheet.nrows)):
            this_month = date_to_month(sheet.cell(row, 0).value)
            value = sheet.cell(row, 1).value

            if value and (type(value) in [float, int, long]):

                if MonthlySentiment.objects.filter(month=this_month, country=settings.COUNTRY):
                    m_sentiment = MonthlySentiment.objects.get(month=this_month, country=settings.COUNTRY)
                else:
                    m_sentiment = MonthlySentiment()

                m_sentiment.month = this_month
                m_sentiment.sentiment = value
                m_sentiment.country = settings.COUNTRY
                m_sentiment.save()
                print 'MonthlySentiment  %s --  Saved.' % str(m_sentiment)
