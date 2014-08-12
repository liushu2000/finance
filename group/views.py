from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from conf import settings
from django_datatables_view.base_datatable_view import BaseDatatableView
from models import *
from django.forms.models import model_to_dict
from django.db import transaction
from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@login_required
def group(request):
    template = settings.SITE + '/group_bootstrap.html'

    return render_to_response(template, context_instance=RequestContext(request))


class CreateGroupWizard(SessionWizardView):
    template_name = settings.SITE + '/create_group_bootstrap.html'

    def dispatch(self, request, *args, **kwargs):
        # check if it is a branch create on branch, redirect to group page with error message.
        if 'group_id_branch' in self.kwargs and 'group_id' not in self.kwargs:
            group_id = self.kwargs['group_id_branch']
            group = GroupBranch.objects.get(id=group_id)

            if group.parent:
                messages.warning(self.request,  _("Warning: Branch cannot be created on branch, please select a group to create branch."))
                return redirect('/group/')
            else:
                return super(CreateGroupWizard, self).dispatch(request, *args, **kwargs)
        else:
                return super(CreateGroupWizard, self).dispatch(request, *args, **kwargs)

    def get_form_initial(self, step):

        # Edit Group/Branch details
        if 'group_id' in self.kwargs and 'group_id_branch' not in self.kwargs:
            group_id = self.kwargs['group_id']
            group = GroupBranch.objects.get(id=group_id)

            group_dict= model_to_dict(group, fields=[], exclude=[])

            initial_data = group_dict

            self.request.page_title = 'Edit Group/Branch Details'
            return initial_data

        # Create New Branch
        elif 'group_id_branch' in self.kwargs and 'group_id' not in self.kwargs:
            group_id = self.kwargs['group_id_branch']
            group = GroupBranch.objects.get(id=group_id)

            initial_data = {'parent': group}
            self.request.page_title = 'Create New Branch for: '+str(group)
            return initial_data

        else:
            # Create New Group
            self.request.page_title = 'Create New Group'
            return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        if 'group_id' in self.kwargs:
            group_id = self.kwargs['group_id']
            new = GroupBranch.objects.get(id=group_id)

        else:
            new = GroupBranch()

        for form in form_list:
            for k, v in form.cleaned_data.iteritems():
                setattr(new, k, v)

        #new['at'] = datetime.datetime.now()

        # Make sure user and group are saved or failed at the same time.
        # with transaction.atomic():
        new.save()

        return HttpResponseRedirect('/group/')


class GroupListJson(BaseDatatableView):
        # The model we're going to show
        # model = Policy

        # define the columns that will be returned
        columns = ['id', 'name', 'parent', 'type', 'phone', 'address']
        #hidden_columns = 'id',
        # define column names that will be used in sorting
        # order is important and should be same as order of columns
        # displayed by datatables. For non sortable columns use empty
        # value like ''
        order_columns = ['id', 'name', 'parent', 'type', 'phone', 'address', ]

        # set max limit of records returned, this is used to protect our site if someone tries to attack our site
        # and make it return huge amount of data
        max_display_length = 100


        # def render_column(self, row, column):
        #     # We want to render user as a custom column
        #     if column == 'name':
        #         return '%s %s' % (row.name, row.email)
        #     else:
        #         return super(UserListJson, self).render_column(row, column)
        def get_initial_queryset(self):

            # return queryset used as base for futher sorting/filtering
            # these are simply objects displayed in datatable
            # You should not filter data returned here by any filter values entered by user. This is because
            # we need some base queryset to count total number of records.
            return GroupBranch.objects.all()


        def filter_queryset(self, qs):


            # simple example:
            sSearch = self.request.GET.get('sSearch', None)

            if sSearch:
                qs = qs.filter(name__icontains=sSearch)

            # more advanced example
            filter_customer = self.request.POST.get('group', None)

            # if filter_customer:
            #     customer_parts = filter_customer.split(' ')
            #     qs_params = None
            #     for part in customer_parts:
            #         q = Q(name__istartswith=part)|Q(holder__istartswith=part)
            #         qs_params = qs_params | q if qs_params else q
            #     qs = qs.filter(qs_params)
            return qs

        def prepare_results(self, qs):
            # prepare list with output column data
            # queryset is already paginated here
            json_data = []
            for item in qs:
                json_data.append([
                    item.id,
                    '',
                    item.name,
                    # str(item.first_name),
                    str(item.parent),
                    item.type,
                    item.phone,
                    item.address,

                ])
            return json_data


from selectable.base import ModelLookup
from selectable.registry import registry


class GroupLookup(ModelLookup):
    model = GroupBranch
    search_fields = ('name__icontains', )
    filters = {'parent__isnull': True, }

registry.register(GroupLookup)