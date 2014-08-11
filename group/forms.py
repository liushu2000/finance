from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from models import *
from views import GroupLookup
import selectable.forms as selectable


class GroupForm(forms.Form):
    group = forms.CharField(
        label='Group:',
        widget=selectable.AutoCompleteSelectField(GroupLookup),
        required=False,
    )


class GroupCreationForm(forms.ModelForm):
    #parent = forms.CharField(widget=forms.HiddenInput())
    #form.fields['field_name'].widget = forms.HiddenInput()
    group = forms.CharField(
        label='Group:',
        widget=selectable.AutoCompleteWidget(GroupLookup),
        required=False,
    )
    class Meta:
        model = GroupBranch
        fields = ("name",  "parent", "type", "phone", "address", "group",)

    def __init__(self, *args, **kwargs):
        super(GroupCreationForm, self).__init__(*args, **kwargs)
        #self.fields['parent'].widget.attrs['disabled'] = True
        # self.fields['parent'].widget.attrs['readonly'] = True
        self.fields['parent'].widget = forms.HiddenInput()
        self.helper = FormHelper()
        self.helper.form_id = 'create_group_form'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
 #       self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-5'
        self.helper.layout = Layout(
            'name',
            'parent',
            'type',
            'phone',
            'address',
            'group',
            #Field('make', css_class='input-xlarge',  help_text='Maximum 8 chars.'),

            FormActions(
                Button('cancel', 'Cancel', css_class="btn-default btn-lg", onclick='window.location.href="{}"'.format('/group/'), style="margin-left:380px"),
                Submit('save_changes', 'Save', css_class=" btn-lg",style="margin-left:10px" ),
                        )
        )
        self.fields['name'].label = "Name:"
        # self.fields['parent'].label = "Group:"
        self.fields['phone'].label = "Phone:"
        self.fields['address'].label = "Address:"

    # applied only if form been used as single form rather than Formwizard
    def save(self, commit=True):
        group = super(GroupCreationForm, self).save(commit=False)
        #user.email = self.cleaned_data["email"]
        if commit:
            group.save()
        return group