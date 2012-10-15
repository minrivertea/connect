from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail


from django.contrib import messages

from website.models import *
from website.forms import *

from datetime import datetime


#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )

def changelang(request, code):
    from django.utils.translation import check_for_language, activate, to_locale, get_language
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    lang_code = code
    print lang_code
    if lang_code and check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response




def index(request):
    return render(request, "website/home.html", locals())

def news_item(request, slug):  
    item = get_object_or_404(News, slug=slug)
    return render(request, 'website/news_item.html', locals())


def page(request, slug, x=None, y=None, z=None):
    page = get_object_or_404(Page, slug=slug)
    
    if x or y or z:
        return HttpResponseRedirect(page.get_absolute_url())
    
    if slug == 'news':
        news_list = News.objects.filter(is_published=True, date_posted__lte=datetime.now()).exclude(title=None)
    
        paginator = Paginator(news_list, 10) # Show 25 contacts per page
    
        # Make sure page request is an int. If not, deliver first page.
        try:
            p = int(request.GET.get('page', '1'))
        except ValueError:
            p = 1
    
        # If page request (9999) is out of range, deliver last page of results.
        try:
            news = paginator.page(p)
        except (EmptyPage, InvalidPage):
            news = paginator.page(paginator.num_pages)
            
        
    template = "website/page.html"
    if page.template:
        template = page.template
        
        
        
    if request.method == 'POST':
        if 'contact' in request.path:
            form = ContactForm(request.POST)
            if form.is_valid():
                
                #send an email to the guys
                body = render_to_string('emails/contact.txt', {
                   'message': form.cleaned_data['message'],
                   'email': form.cleaned_data['email'],
                   'name': form.cleaned_data['name'],  
                })
                recipient = settings.SITE_EMAIL
                sender = settings.SITE_EMAIL
                subjectline = "WEBSITE CONTACT SUBMISSION"
                
                send_mail(
                              subjectline, 
                              body, 
                              sender,
                              [recipient], 
                              fail_silently=False
                )
                
                # message for the user
                message = "Thanks, your message has been sent and we'll get back to you ASAP!"
                messages.add_message(request, messages.INFO, message)
                
                url = request.META.get('HTTP_REFERER', None)
                return HttpResponseRedirect(url)
    
    return render(request, template, locals())