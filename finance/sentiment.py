__author__ = 'shu'
from itertools import groupby
from scipy import stats
from xlrd import open_workbook
from models import *
from conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from import_data import date_to_month
import numpy
from django.db.models import Count
import numpy as np
import math
from django.db.models import Avg
import datetime
from import_data import cut


def generate_monthly_groups(input_types=None):
    input_types = ['sales', 'std', 'market_value', 'book_market_value']
    # input_types = ['sales', ]
    for input_type in input_types:
        for monthly_sentiment in MonthlySentiment.objects.filter(country=settings.COUNTRY).exclude(sentiment=None):
            this_month = monthly_sentiment.month

            #if this_month == datetime.datetime.strptime('1990-01-01', '%Y-%m-%d').date():

            first = datetime.date(day=1, month=this_month.month, year=this_month.year)
            last_month = first - datetime.timedelta(days=1)
            last_month = datetime.datetime.strptime(last_month.strftime("%Y%m"), "%Y%m")

            monthly_result_list = []
            for count, cm in enumerate(CompanyMonthly.objects.filter(month=this_month, company__country=settings.COUNTRY).exclude(returns=None).order_by(input_type)):
                monthly_result_list.append(cm)

            monthly_groups = cut(monthly_result_list, 10)

            if monthly_groups:
                for idx, group in enumerate(monthly_groups):
                    l = []
                    for c_m in group:
                        l.append(c_m.returns)
                    group_avg = np.mean(l)

                    # group_avg = group.aggregate(Avg('returns'))
                    if MonthlyGroups.objects.filter(month=this_month, type=input_type, country=settings.COUNTRY, group_number=idx):
                        m_group = MonthlyGroups.objects.get(month=this_month, type=input_type, country=settings.COUNTRY, group_number=idx)
                    else:
                        m_group = MonthlyGroups()
                    if MonthlySentiment.objects.filter(country=settings.COUNTRY, month=last_month).exclude(sentiment=None):
                        lastmonth_sentiment = MonthlySentiment.objects.get(country=settings.COUNTRY, month=last_month).sentiment
                        if lastmonth_sentiment >= 0:
                            m_group.lastmonth_sentiment = 1
                        else:
                            m_group.lastmonth_sentiment = -1
                    m_group.country = settings.COUNTRY
                    m_group.month = this_month
                    m_group.group_number = idx
                    m_group.type = input_type
                    m_group.average_returns = group_avg
                    m_group.save()
                    print 'Monthly Group number:%s of %s Average Returns (based on %s) is: %s - Saved.' % (str(idx), str(m_group), input_type, group_avg)


def monthly_groups_companre(input_types=None):
    input_types = ['sales', 'std', 'market_value', 'book_market_value']
    # input_types = ['std']

    for input_type in input_types:
        mg_plus_group = MonthlyGroups.objects.filter(type=input_type, country=settings.COUNTRY, lastmonth_sentiment=1).values('group_number').annotate(average=Avg('average_returns'))
        mg_minus_group = MonthlyGroups.objects.filter(type=input_type, country=settings.COUNTRY, lastmonth_sentiment=-1).values('group_number').annotate(average=Avg('average_returns'))
        i=0
        for i in range(10):
            avg = mg_plus_group[i]['average'] - mg_minus_group[i]['average']
            if MonthlyGroupsResult.objects.filter(group_number=i, type=input_type, country=settings.COUNTRY):
                mg_result = MonthlyGroupsResult.objects.get(group_number=i, type=input_type, country=settings.COUNTRY)
            else:
                mg_result = MonthlyGroupsResult()
            mg_result.group_number = i
            mg_result.type = input_type
            mg_result.country = settings.COUNTRY
            mg_result.result = avg
            mg_result.save()

            print 'Group Compare Result for group %s type -- %s -- is %s -- Saved.' % (str(i), input_type, str(avg))