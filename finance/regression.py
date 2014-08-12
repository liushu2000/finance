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
from datetime import datetime



def regression(request):
    result = []

    company_alpha_beta()
    monthly_std()


    template = 'home.html'

    return render_to_response(template,
                              {"result": result,  },
                              context_instance=RequestContext(request))


def residual(real_return, intercept, gradient, market_return, date_posted, ):
    residual_result = real_return - intercept - gradient*market_return
    this_month = date_to_month(date_posted)
    result = [this_month, residual_result, ]
    return result


def company_alpha_beta():
    for company in Company.objects.filter(country=settings.COUNTRY, ):
        real_return_list = []
        rm_rf_list = []
        for cd in CompanyDaily.objects.filter(company=company).exclude(real_returns=None):
            if DailyRF.objects.filter(date=cd.date).exclude(rm_rf=None):
                real_return_list.append(cd.real_returns)
                rm_rf_list.append(DailyRF.objects.get(date=cd.date).rm_rf)
        if real_return_list and rm_rf_list:
            gradient, intercept, r_value, p_value, std_err = stats.linregress(real_return_list, rm_rf_list)
            company.alpha = intercept
            company.beta = gradient
            company.save()


def monthly_std():
    for company in Company.objects.filter(country=settings.COUNTRY).exclude(alpha=None).exclude(beta=None):
        residual_list = []
        for cd in CompanyDaily.objects.filter(company=company).exclude(real_returns=None):
            if DailyRF.objects.filter(date=cd.date, country=settings.COUNTRY).exclude(rm_rf=None):
                rm_rf = DailyRF.objects.get(date=cd.date, country=settings.COUNTRY).rm_rf
                residual_value = residual(cd.real_returns, company.alpha, company.beta, rm_rf, cd.date,)
                residual_list.append(residual_value)

        monthly_std_list = []
        for month, group in groupby(residual_list, key=lambda x: x[0]):
            monthly_residuals = []
            for value in group:
                monthly_residuals.append(value[1])
                #monthly_std.append(group)
            monthly_std = numpy.std(monthly_residuals)
            monthly_std_list.append([month, monthly_std])


            this_month = month
            if CompanyMonthly.objects.filter(company=company, month=this_month):
                company_monthly = CompanyMonthly.objects.get(company=company, month=this_month)
            else:
                company_monthly = CompanyMonthly()
            company_monthly.company = company
            company_monthly.month = this_month
            company_monthly.std = monthly_std
            company_monthly.save()


cut = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
def monthly_vp(request, measure_type=None):
    result = []
    measure_type = 'std'
    measure_type = 'returns'

    all = CompanyMonthly.objects.all().values('month').annotate(company_count=Count('company')).order_by('month')
    all_months = [i['month'] for i in all]
    for idx, this_month in enumerate(all_months):
        monthly_companies = CompanyMonthly.objects.filter(month=this_month).order_by(measure_type)
        groups = cut(monthly_companies, 10)
        top_groups = groups[:2]

        a= []
        for g in top_groups:
            for c in g:
                if c.market_value and c.book_value:
                    a.append(c.market_value / c.book_value)

        a_mean = np.mean(a)

        buttom_groups = groups[-3:]
        b= []
        for g in buttom_groups:
            for c in g:
                if c.market_value and c.book_value:
                    b.append(c.market_value / c.book_value)
        b_mean = np.mean(b)

        if not math.isnan(a_mean) and not math.isnan(b_mean):
            m_v_premium= a_mean/b_mean
            result.append(m_v_premium)
            print "++++++++++++++++++++++++++++++++++++"
            print str(type(m_v_premium))
            print m_v_premium
            if MonthlyVP.objects.filter(month=this_month):
                monthly_vp = MonthlyVP.objects.get(month=this_month)
            else:
                monthly_vp = MonthlyVP()
            monthly_vp.vp = m_v_premium
            monthly_vp.month = this_month
            monthly_vp.country = settings.COUNTRY
            monthly_vp.save()
    template = 'home.html'

    return render_to_response(template,
                              {"result": result,  },
                              context_instance=RequestContext(request))