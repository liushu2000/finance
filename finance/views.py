from django.shortcuts import render
from models import *
from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext



def home(request):
    template = 'home.html'

    return render_to_response(template, context_instance=RequestContext(request))