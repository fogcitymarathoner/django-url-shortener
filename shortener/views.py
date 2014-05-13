import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
#from django.views.generic import list_detail
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.db import transaction
from django.conf import settings

from urlweb.shortener.baseconv import base62
from urlweb.shortener.models import Link, LinkSubmitForm

def follow(request, base62_id):
    """ 
    View which gets the link for the given base62_id value
    and redirects to it.
    """
    key = base62.to_decimal(base62_id)
    link = get_object_or_404(Link, pk = key)
    link.usage_count += 1
    link.save()
    return HttpResponsePermanentRedirect(link.url)

def default_values(request, link_form=None):
    """ 
    Return a new object with the default values that are typically
    returned in a request.
    """
    if not link_form:
        link_form = LinkSubmitForm()
    #allowed_to_submit = is_allowed_to_submit(request)
    allowed_to_submit = True
    return { 'show_bookmarklet': allowed_to_submit,
             'show_url_form': allowed_to_submit,
             'site_name': settings.SITE_NAME,
             'site_base_url': settings.SITE_BASE_URL,
             'link_form': link_form,
             }

def info(request, base62_id):
    """
    View which shows information on a particular link
    """
    key = base62.to_decimal(base62_id)
    link = get_object_or_404(Link, pk = key)
    values = default_values(request)
    values['link'] = link
    return render_to_response(
        'shortener/link_info.html',
        values,
        context_instance=RequestContext(request))

def submit(request):
    """
    View for submitting a URL
    """
    #if settings.REQUIRE_LOGIN and not request.user.is_authenticated():
        # TODO redirect to an error page
        #raise Http404
    url = None
    link_form = None
    if request.GET:
        link_form = LinkSubmitForm(request.GET)
    elif request.POST:
        link_form = LinkSubmitForm(request.POST)
    if link_form and link_form.is_valid():
        url = link_form.cleaned_data['u']
        link = None
        try:
            link = Link.objects.get(url = url)
        except Link.DoesNotExist:
            pass
        if link == None:
            new_link = Link(url = url)
            new_link.save()
            link = new_link
        values = default_values(request)
        values['link'] = link
        return render_to_response(
            'shortener/submit_success.html',
            values,
            context_instance=RequestContext(request))
    values = default_values(request, link_form=link_form)
    return render_to_response(
        'shortener/submit_failed.html',
        values,
        context_instance=RequestContext(request))

def soap(request):
    """
    View for submitting a URL, as a service
    """
    #if settings.REQUIRE_LOGIN and not request.user.is_authenticated():
        # TODO redirect to an error page
        #raise Http404
    url = None
    link_form = None
    print request.POST
    if request.GET:
        link_form = LinkSubmitForm(request.GET)
    elif request.POST:
        url =  request.POST['u']
        link = None
        try:
            link = Link.objects.get(url = url)
        except Link.DoesNotExist:
            pass
        if link == None:
            new_link = Link(url = url)
            new_link.save()
            link = new_link
        values = default_values(request)
        values['link'] = link
        return render_to_response(
            'shortener/soap_result.html',
            values,
            context_instance=RequestContext(request))
    values = default_values(request, link_form=link_form)
    return render_to_response(
        'shortener/submit_failed.html',
        values,
        context_instance=RequestContext(request))



    if link_form and link_form.is_valid():
        url = link_form.cleaned_data['u']
        print url
        link = None
        try:
            link = Link.objects.get(url = url)
        except Link.DoesNotExist:
            pass
        if link == None:
            new_link = Link(url = url)
            new_link.save()
            link = new_link
        values = default_values(request)
        values['link'] = link
        return render_to_response(
            'shortener/soap_result.html',
            values,
            context_instance=RequestContext(request))
    values = default_values(request, link_form=link_form)
    return render_to_response(
        'shortener/submit_failed.html',
        values,
        context_instance=RequestContext(request))

def index(request):
    """
    View for main page (lists recent and popular links)
    """
    values = default_values(request)
    values['recent_links'] = Link.objects.all().order_by('-date_submitted')[0:10]
    values['most_popular_links'] = Link.objects.all().order_by('-usage_count')[0:10]
    return render_to_response(
        'shortener/index.html',
        values,
        context_instance=RequestContext(request))

def is_allowed_to_submit(request):
    """
    Return true if user is allowed to submit URLs
    """
    return not settings.REQUIRE_LOGIN or request.user.is_authenticated()


from django.views.generic.list import ListView
from django.utils import timezone


class LinkListView(ListView):
    queryset = Link.objects.order_by('-date_submitted')[:10]
    model = Link
    """
	FIXME
	cannot override link_list.html !!!!
    template_name = 'index.html'
    """
    def get_context_data(self, **kwargs):
        context = super(LinkListView, self).get_context_data(**kwargs)
	context['most_popular'] = Link.objects.order_by('-usage_count')[:10]
	context['show_url_form'] = True
        context['link_form'] = LinkSubmitForm()
        return context
