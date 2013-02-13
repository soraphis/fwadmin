from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.urlresolvers import reverse
from fwadmin.models import (
    Host,
    Port,
    HostPort,
)

def new(request):
    print "new", request
    pass
