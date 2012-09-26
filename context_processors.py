from django.conf import settings
from website.models import *

def common(request):
    import settings
    context = {}
    try:
        homepage = HomePage.objects.filter(is_active=True, lang=request.LANGUAGE_CODE)[0]
    except:
        homepage = None
        
    
    try:
        tagline = homepage.logo_tagline
    except:
        tagline = None
    
    
    context['homepage'] = homepage    
    context['tagline'] = tagline
    context['topnav'] = Page.objects.filter(is_top_nav=True).exclude(title=None).order_by('top_nav_position')
    context['ga_is_on'] = settings.GA_IS_ON
    context['testimonials'] = Page.objects.filter(is_client_testimonial=True).exclude(title=None, image=None)
    return context
    
