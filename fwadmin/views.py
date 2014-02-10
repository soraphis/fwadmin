import collections
import datetime
import json
import StringIO
import socket

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from .auth import (
    group_required,
    NotOwnerError,
    user_has_permssion_for_host
)

from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponse,
)
from django.shortcuts import (
    render_to_response,
    redirect,
)
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import (
    login_required,
)
from fwadmin.models import (
    ComplexRule,
    Host,
)
from fwadmin.forms import (
    NewHostForm,
    EditHostForm,
    NewRuleForm,
)
from fwadmin.genrules import gen_firewall_rules
from fwadmin.utils import log
from django.conf import settings


# FIXME: find a even better location
def get_quick_buttons():
    Button = collections.namedtuple(
        "Button", ["name", "description", "ip_protocol", "port"]
    )
    quick_buttons = [
        Button("ssh", "Secure Shell (SSH)", "TCP", "22"),
        Button("http", "Hypertext (HTTP)", "TCP", "80"),
        Button("https", "Secure Hypertext (HTTPS)", "TCP", "443"),
    ]
    return quick_buttons


@login_required
@group_required(settings.FWADMIN_ALLOWED_USER_GROUP)
def index(request):
    all_hosts = Host.objects.filter(owner=request.user)
    all_hosts |= Host.objects.filter(owner2=request.user)
    # pass all views that the user owns too
    return render_to_response('fwadmin/index.html',
                              {'all_hosts': all_hosts,
                              },
                              context_instance=RequestContext(request))


@login_required
@group_required(settings.FWADMIN_MODERATORS_USER_GROUP)
def export(request, fwtype):
    outs = StringIO.StringIO()
    gen_firewall_rules(outs, fwtype)
    return HttpResponse(outs.getvalue(), content_type="text/plain")


@login_required
@group_required(settings.FWADMIN_ALLOWED_USER_GROUP)
def new_host(request):
    if request.method == 'POST':
        form = NewHostForm(request.POST, owner_username=request.user)
        if form.is_valid():
            # do not commit just yet, we need to add more stuff
            host = form.save(commit=False)
            # add the stuff here that the user can't edit
            host.owner = request.user
            active_until = (
                datetime.date.today() +
                datetime.timedelta(settings.FWADMIN_DEFAULT_ACTIVE_DAYS))
            host.active_until = active_until
            # and really save
            host.save()

            # and log
            log(host,
                request.user,
                "New host %s (%s) created" % (host.name, host.ip))

            messages.success(request,
                _("Host %s succefully created.") % host.name)

            return HttpResponseRedirect(reverse("fwadmin:new_rule_for_host",
                                                args=(host.id,)))
    else:
        form = NewHostForm(owner_username=request.user)
    return render_to_response('fwadmin/host/new.html',
                              {'form': form,
                              },
                              context_instance=RequestContext(request))


@login_required
@group_required(settings.FWADMIN_ALLOWED_USER_GROUP)
def renew_host(request, pk):
    host = Host.objects.filter(pk=pk)[0]
    if not user_has_permssion_for_host(host, request.user):
        return NotOwnerError(request.user)
    active_until = (datetime.date.today() +
                    datetime.timedelta(settings.FWADMIN_DEFAULT_ACTIVE_DAYS))
    host.active_until = active_until
    host.save()

    # and log
    log(host,
        request.user,
        "Renew host %s (%s)" % (host.name, host.ip))

    messages.success(request,
        _('Thanks for renewing, host firewall active until %s.' %
            active_until))

    return redirect(reverse("fwadmin:index"),
                        context_instance=RequestContext(request))


@login_required
@group_required(settings.FWADMIN_ALLOWED_USER_GROUP)
def delete_host(request, pk):
    host = Host.objects.get(pk=pk)
    if not user_has_permssion_for_host(host, request.user):
        return NotOwnerError(request.user)
    if request.method == 'POST':
        # and log
        log(host,
            request.user,
            "Delete host %s (%s)" % (host.name, host.ip))

        host.delete()

        messages.success(request, _("Host %s was deleted.") % host.name)
        return redirect(reverse("fwadmin:index"),
                        context_instance=RequestContext(request))
    return HttpResponseBadRequest("Only POST supported here")


@login_required
@group_required(settings.FWADMIN_ALLOWED_USER_GROUP)
def edit_host(request, pk):
    host = Host.objects.filter(pk=pk)[0]
    if not user_has_permssion_for_host(host, request.user):
        return NotOwnerError(request.user)
    if request.method == 'POST':
        form = EditHostForm(request.POST, instance=host)
        if form.is_valid():
            # and log
            log(host,
                request.user,
                "Edit host %s (%s)\n\nChanges: %r" % (host.name,
                                                    host.ip,
                                                    host.diff))

            form.save()

            return HttpResponseRedirect(reverse("fwadmin:index"))
    else:
        form = EditHostForm(instance=host)
    rules_list = ComplexRule.objects.filter(host=host)
    return render_to_response('fwadmin/host/edit.html',
                              {'form': form,
                               'host': host,
                               'rules_list': rules_list,
                              },
                              context_instance=RequestContext(request))


@login_required
@group_required(settings.FWADMIN_MODERATORS_USER_GROUP)
def moderator_list_unapproved(request):
    all_hosts = Host.objects.filter(approved=False)
    # XXX: add a template for list
    return render_to_response('fwadmin/admin/unapproved_hosts.html',
                              {'all_hosts': all_hosts,
                               },
                              context_instance=RequestContext(request))


@login_required
@group_required(settings.FWADMIN_MODERATORS_USER_GROUP)
def moderator_list_all(request):
    all_hosts = Host.objects.all()
    # XXX: add a template for list
    return render_to_response('fwadmin/admin/all_hosts.html',
                              {'all_hosts': all_hosts,
                               },
                              context_instance=RequestContext(request))


@login_required
@group_required(settings.FWADMIN_MODERATORS_USER_GROUP)
def moderator_approve_host(request, pk):
    # FIXME: form for CSRF protection (?)
    host = Host.objects.get(pk=pk)
    host.approved = True
    host.save()

    # and log
    log(host,
        request.user,
        "Host %s (%s) approved" % (host.name, host.ip))

    messages.success(request, _("Host %s approved.") % host.name)
    return redirect(reverse("fwadmin:moderator_list_unapproved"),
                    context_instance=RequestContext(request))


@login_required
@group_required(settings.FWADMIN_ALLOWED_USER_GROUP)
def delete_rule(request, pk):
    if request.method == 'POST':
        rule = ComplexRule.objects.get(pk=pk)
        host = rule.host
        if not user_has_permssion_for_host(host, request.user):
            return NotOwnerError(request.user)
        rule.delete()

        # and log
        log(host,
            request.user,
            "Delete Rule %s (%s/%s)" % (rule, host.name, host.ip))

        messages.success(request, _("Rule %s was deleted.") % rule.name)

        return redirect("%s#tab-rules" %
            reverse("fwadmin:edit_host", args=(host.id,)))
    return HttpResponseBadRequest("Only POST supported here")


@login_required
@group_required(settings.FWADMIN_ALLOWED_USER_GROUP)
def new_rule_for_host(request, hostid):
    host = Host.objects.get(pk=hostid)
    if not user_has_permssion_for_host(host, request.user):
        return NotOwnerError(request.user)
    if request.method == 'POST':
        form = NewRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.host = host
            stock_port = form.cleaned_data["stock_port"]
            if stock_port:
                rule.ip_protocol = stock_port.ip_protocol
                rule.port_range = stock_port.number
            rule.save()

            log(rule.host,
                request.user,
                "New rule %s" % rule)

            return HttpResponseRedirect("%s#tab-rules" %
                reverse("fwadmin:edit_host", args=(host.id,)))
    else:
        form = NewRuleForm()
    return render_to_response('fwadmin/rule/new.html',
                              {'host': host,
                               'form': form,
                               'quick_buttons': get_quick_buttons(),
                              },
                              context_instance=RequestContext(request))


def gethostbyname(request, hostname):
    try:
        addresslist = socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror:
        addresslist = []
    return HttpResponse(
        json.dumps(addresslist), content_type="application/json")
