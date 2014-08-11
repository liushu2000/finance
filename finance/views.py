from django.shortcuts import render
from models import CompanyMonthly
from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
import numpy as np

cut = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

def make_groups(request, measure_type=None):
    result = []
    measure_type = 'std'
    measure_type = 'returns'
    input_month = datetime.strptime('1990-01-01', '%Y-%m-%d')
    all_company_monthly =  CompanyMonthly.objects.all()
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
        if a_mean and b_mean:
            m_v_premium= a_mean/b_mean
            result.append(m_v_premium)
    # result = all_months
    template = 'done.html'

    return render_to_response(template,
                              {"result": result, 'title': measure_type },
                              context_instance=RequestContext(request))