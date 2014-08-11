from scipy import stats
from xlrd import open_workbook, xldate_as_tuple
import xlsxwriter
from datetime import datetime, timedelta
import numpy
import itertools
#from scipy import stats
#from rpy import r
# from numpy import arange,array,ones,linalg
# from pylab import plot,show

data = open_workbook('/home/shu/Downloads/uk_data.xlsx',)
workbook = xlsxwriter.Workbook('/home/shu/Downloads/uk_data_result.xlsx')
# data = open_workbook('/home/shu/Downloads/simple.xlsx', on_demand=True)
# workbook = xlsxwriter.Workbook('/home/shu/Downloads/simple_result.xlsx')
sheets_names = data.sheet_names()
new_prices_sheets_list = [i for i in sheets_names if 'daily price' in i]

# ------------------Market return rates into Dict-------------------------
#market_return_book_sheet = market_return_book.sheets()[0]
#market_return_dict = dict(zip(market_return_book_sheet.col_values(0), market_return_book_sheet.col_values(1)))


for sheet_name in new_prices_sheets_list:
    sheet = data.sheet_by_name(sheet_name)
    worksheet = workbook.add_worksheet(sheet_name+" return")
    column=0
    row=0
    market_return_list = sheet.col(1)
    rm_rf_list = filter(None, [i.value for i in sheet.col(2)])
    print "rm_rf_list", rm_rf_list

    # --------------------------------------- Page Row 1-------------------------
    column_titles=sheet.row(0)
    column=0
    for idx, column_title in enumerate(column_titles):
        # print "------------------"+ str(type(column_title))
        worksheet.write(0, column, column_title.value)
        column+=1

    # --------------------------------------- Company code Row 2-------------------------
    company_codes=sheet.row(1)
    column=0
    for company_code in company_codes:
        # print "------------------"+ str(type(column_title))
        worksheet.write(1, column, company_code.value)
        column+=1

    # --------------------------------------- Page Column 1 Date/Month/Year-------------------------
    row_titles=sheet.col(0)
    row=2


    for row_title in row_titles[2:]:
        # convert excel date format to python datetime format
        #datetime_value = datetime(*xldate_as_tuple(row_title.value, 0))
        datetime_value = row_title.value
        #print "------------------"+ str(row_title)
        worksheet.write(row, 0, datetime_value)
        row += 1

    # --------------------------------------- Return Values -------------------------

    for column in range(1,sheet.ncols):
        #row = 3
        count = 0

        return_list = []
        not_empty_list = []
        for idx, row in enumerate(range(2, sheet.nrows)):
            shell = sheet.cell(row,column).value
            #print "------------------"+ str(type(shell))
            count+=1
            if count <> 1 and not isinstance(shell, str) and not isinstance(shell_previous, str):
                # print "------------------"+ str(row)  +"---------------"+  str(market_return_list[idx])
                return_list.append((shell/shell_previous) -1)

            shell_previous = shell

        row = 3

        for value in return_list:

            worksheet.write(row, column, value)
            row +=1

workbook.close()



