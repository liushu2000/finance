from scipy import stats
from xlrd import open_workbook, xldate_as_tuple
import xlsxwriter
from datetime import datetime, timedelta
import numpy
import itertools
from itertools import groupby
from models import CompanyMonthly
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import re

def residual(real_return, intercept, gradient, market_return, date_posted, comany):
    residual_result = real_return - intercept - gradient*market_return
    this_month = date_to_month(date_posted)
    result = [this_month, comany, residual_result, ]
    return result

# excel = '/home/shu/Downloads/simple_value.xlsx'
# excel = '/home/shu/Downloads/simple_result.xlsx'
excel = '/home/shu/projects/django/finance/data/uk_data.xlsx'
excel2 = '/home/shu/projects/django/finance/data/uk_data_result.xlsx'
# excel_result ='/home/shu/Downloads/simple_regression_result.xlsx'
excel_result ='/home/shu/projects/django/finance/data/uk_regression_result.xlsx'


def date_to_month(input_date):
    if type(input_date) == float:
        seconds = (input_date - 25569) * 86400.0
        time = datetime.utcfromtimestamp(seconds)
        date = time.date()
    else:
        date = datetime.strptime(input_date, '%d/%m/%Y').date()
    month = str(date.year) + '-'+ str(date.month)
    this_month = datetime.strptime(month, '%Y-%m')
    return this_month


def company_monthly(request):

    monthly_std()
    monthly_market_value()
    monthly_book_value()
    monthly_sales()
    monthly_return()
    template = 'done.html'

    return render_to_response(template, context_instance=RequestContext(request))

def monthly_std():
    data = open_workbook(excel2, on_demand=True)
    workbook = xlsxwriter.Workbook(excel_result)
    sheets_names = data.sheet_names()
    new_prices_sheets_list = [i for i in sheets_names if 'daily price' and 'return' in i]

    for sheet_name in new_prices_sheets_list:
        sheet = data.sheet_by_name(sheet_name)
        worksheet = workbook.add_worksheet(sheet_name+" reg")
        column = 0
        row = 0
        market_return_list = sheet.col(1)
        rm_rf_list = filter(None, [i.value for i in sheet.col(2)])
        print "rm_rf_list", rm_rf_list

        # --------------------------------------- Page Row 1-------------------------
        column_titles = sheet.row(0)
        column = 0
        for idx, column_title in enumerate(column_titles):
            # print "------------------"+ str(type(column_title))
            worksheet.write(0, column, column_title.value)
            column += 1

        # --------------------------------------- Company code Row 2-------------------------
        company_codes = sheet.row(1)
        column = 0
        for company_code in company_codes:
            # print "------------------"+ str(type(column_title))
            worksheet.write(1, column, company_code.value)
            column += 1

        # --------------------------------------- Page Column 1 Date/Month/Year-------------------------
        row_titles = sheet.col(0)
        row = 2

        for row_title in row_titles[2:]:
            # convert excel date format to python datetime format
            #datetime_value = datetime(*xldate_as_tuple(row_title.value, 0))
            date_value = row_title.value
            #print "------------------"+ str(row_title)
            worksheet.write(row, 0, date_value)
            row += 1
        worksheet.write(sheet.nrows+2, 0, 'Alpha')
        worksheet.write(sheet.nrows+3, 0, 'Beta')
        worksheet.write(sheet.nrows+4, 0, 'STD')
        # --------------------------------------- Return Values -------------------------

        for column in range(3, sheet.ncols):

            #row = 3
            count = 0
            company = sheet.cell(0, column).value
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]
            real_return_list = []
            # not_empty_list = []
            rm_rf_list = []
            for idx, row in enumerate(range(2, sheet.nrows)):

                return_value = sheet.cell(row,column).value
                rf = sheet.cell(row,1).value
                if return_value and rf:

                    real_return = float(return_value)- float(rf)
                    count += 1
                    # colum 1 is risk free rate, col2 is Rm-Rf
                    if (type(return_value) in [float,int,long]) and (type(sheet.cell(row, 2).value) in [float, int, long,complex]):
                        real_return_list.append(real_return)
                        rm_rf_list.append(sheet.cell(row, 2).value)
            # print "++++++++++++++++++++++++++++++++++++"
            # print real_return_list
            # print rm_rf_list
            if real_return_list and rm_rf_list:
                gradient, intercept, r_value, p_value, std_err = stats.linregress(real_return_list,rm_rf_list)
                print "b and a", gradient, intercept
                worksheet.write(sheet.nrows+2, column, intercept)
                worksheet.write(sheet.nrows+3, column, gradient)

                # write residual
                residual_list = []
                for idx, row in enumerate(range(2, sheet.nrows)):
                    date = sheet.cell(row, 0).value
                    if intercept and type(return_value) in [float,int,long] and type(sheet.cell(row, 2).value) in [float,int,long]:
                        residual_value = residual(real_return, intercept, gradient, sheet.cell(row, 2).value, date, company)

                        print residual_value
                        print str(type(residual_value[0]))
                        worksheet.write(row, column, residual_value[2])
                        residual_list.append(residual_value)
                # if residual_list:
                #     std = numpy.std(residual_list)
                #     worksheet.write(sheet.nrows+4, column, std)
                monthly_std_list = []
                #print residual_list
                for month, group in groupby(residual_list, key=lambda x: x[0]):
                    monthly_residuals = []
                    for value in group:
                        monthly_residuals.append(value[2])
                        #monthly_std.append(group)
                    monthly_std = numpy.std(monthly_residuals)
                    monthly_std_list.append([month, company, monthly_std])


                    this_month = month
                    if CompanyMonthly.objects.filter(code=company_code, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(code=company_code, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()
                    company_monthly.company = company
                    company_monthly.code = company_code
                    company_monthly.month = this_month
                    company_monthly.std = monthly_std
                    company_monthly.save()
    workbook.close()


def monthly_market_value():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'market value' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):
            company = sheet.cell(0, column).value
            company = re.sub(" - MARKET VALUE", "", company,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value

                if value and (type(value) in [float, int, long]):

                    if CompanyMonthly.objects.filter(code=company_code, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(code=company_code, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.code = company_code
                    company_monthly.month = this_month
                    company_monthly.market_value = value
                    print company_monthly
                    company_monthly.save()

def monthly_book_value():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'book value' in i]
    # print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    # print sheets_names
    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):
            company = sheet.cell(0, column).value
            company_code = sheet.cell(1, column).value
            company = re.sub(" - BOOK VALUE-OUT SHARES-FISCAL", "", company,)
            company_code = (company_code.split("("))[0]

            for idx, row in enumerate(range(2, sheet.nrows)):
                # date = datetime.strptime(sheet.cell(row, 0).value, '%d/%m/%Y').date()
                # month = str(date.year) + '-'+ str(date.month)
                # this_month = datetime.strptime(month, '%Y-%m')
                this_month = date_to_month(sheet.cell(row, 0).value)
                value = sheet.cell(row, column).value

                if value and (type(value) in [float, int, long]):

                    if CompanyMonthly.objects.filter(code=company_code, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(code=company_code, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.code = company_code
                    company_monthly.month = this_month
                    company_monthly.book_value = value
                    company_monthly.save()
                # else:
                #     print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                #     print value

def monthly_sales():
    data = open_workbook(excel, on_demand=True)
    sheets_names = data.sheet_names()
    sheets_list = [i for i in sheets_names if 'sale' in i]

    for sheet_name in sheets_list:
        sheet = data.sheet_by_name(sheet_name)

        for column in range(1, sheet.ncols):
            company = sheet.cell(0, column).value
            company = re.sub(" - SALES PER SHARE", "", company,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]

            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value

                if value and (type(value) in [float, int, long]):

                    if CompanyMonthly.objects.filter(code=company_code, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(code=company_code, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.code = company_code
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
            company = sheet.cell(0, column).value
            company = re.sub(" - SALES PER SHARE", "", company,)
            company_code = sheet.cell(1, column).value
            company_code = (company_code.split("("))[0]

            # value_previous = 1
            for idx, row in enumerate(range(2, sheet.nrows)):
                this_month = date_to_month(sheet.cell(row, 0).value)

                value = sheet.cell(row, column).value
                if idx > 5 and value and (type(value) in [float, int, long])and value_previous:
                    # print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    # print idx
                    return_value = (value/value_previous) -1


                    if CompanyMonthly.objects.filter(code=company_code, month=this_month):
                        company_monthly = CompanyMonthly.objects.get(code=company_code, month=this_month)
                    else:
                        company_monthly = CompanyMonthly()

                    company_monthly.company = company
                    company_monthly.code = company_code
                    company_monthly.month = this_month
                    company_monthly.returns = return_value
                    company_monthly.save()
                if value:
                    value_previous = value