from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse



from tinymce import models as tinymce_models



class HomePage(models.Model):
    is_active = models.BooleanField(default=True)
    identifier = models.CharField(max_length=200, null=True, blank=True, default="homepage",
        help_text="An optional name you give the homepage to remind you which one it is!")
    
    logo_tagline = models.CharField(max_length=200, blank=True, null=True,
        help_text="A tagline that appears near the logo in the header of all pages.")
    
    intro_box_1 = tinymce_models.HTMLField(help_text="Use Heading3 and Paragraph only!")
    intro_box_1_page = models.ForeignKey('Page', related_name="intro_box_1",
        help_text="Which page does this box link to?")
    intro_box_1_text = models.CharField(max_length=200,
        help_text="The words which appear in the button")
    
    intro_box_2 = tinymce_models.HTMLField()
    intro_box_2_page = models.ForeignKey('Page', related_name="intro_box_2")
    intro_box_2_text = models.CharField(max_length=200)
    
    intro_box_3 = tinymce_models.HTMLField()
    intro_box_3_page = models.ForeignKey('Page', related_name="intro_box_3")
    intro_box_3_text = models.CharField(max_length=200)
    
    twin_box_1 = tinymce_models.HTMLField(null=True, blank=True)
    twin_box_2 = tinymce_models.HTMLField(null=True, blank=True)
    
    long_box = tinymce_models.HTMLField(null=True, blank=True)
    
    image_promo_image = models.ImageField(upload_to='images/promo',
        help_text="A large image spanning the whole page. 960px wide or more please!")
    image_promo_text = models.CharField(max_length=200)
    image_promo_page = models.ForeignKey('Page', related_name="image_promo_text")
    image_promo_link = models.URLField(null=True, blank=True)
    
    meta_title = models.CharField(max_length=200, null=True, blank=True,
        help_text="The title of the page, appears in search engines.")
    meta_description = models.TextField(null=True, blank=True,
        help_text="A description of the website - useful for search engines.")
    meta_keywords = models.TextField(null=True, blank=True,
        help_text="Keywords related to this website.")
    
    
    google_analytics = models.TextField(help_text="The code snippet from Google Analytics used to track your customers. Include the script tags please!",
        blank=True, null=True)
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES,
        help_text="Which language is this variation of the homepage?")
    
    def __unicode__(self):
        return self.identifier
        
       

class News(models.Model):
    date_posted = models.DateTimeField(help_text="Set this to a date in the future to do scheduled posting of news.")
    slug = models.SlugField(help_text="The URL of the page - only dashes and lowercase a-z characters please!")
    title = models.CharField(max_length=256, help_text="Name of the news item.")
    link = models.URLField(help_text="The external URL you will link this story to. Please include the opening http://")
    summary = models.TextField(help_text="A short summary of the item (appears in listings)")
    text = tinymce_models.HTMLField()
    news_type = models.CharField(max_length=100, choices=settings.NEWS_TYPES)
    image = models.ImageField(upload_to='images/news', blank=True, null=True,
        help_text="An optional image; larger than 200px wide please!")
    is_published = models.BooleanField(default=False,
        help_text="Uncheck this to remove item from the website but continue editing (draft).")
    
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        url = reverse('news_item', args=[self.slug])
        return url
    
    def get_link_domain(self):
        from urlparse import urlparse
        url = urlparse(self.link).netloc
        return url



class RightBox(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True,
        help_text="Optional title of the box (appears on the page)")
    
    PROJECT = 'project.html'
    CONTACT = 'contact.html'
    SOCIAL = 'social.html'
    RIGHT_BOXES = (
        (PROJECT, u"Project"),
        (SOCIAL, u"Social"),
        (CONTACT, u"Contact Us"),
    )
        

    template = models.CharField(max_length=200, choices=RIGHT_BOXES, default=PROJECT, 
        help_text="Choose which kind of box it is")
    content = tinymce_models.HTMLField(blank=True, null=True,
        help_text="The text content of the box")
    image = models.ImageField(null=True, blank=True, upload_to="images/right-boxes",
        help_text="An optional image to appear in the box. At least 200px wide please!")
    link = models.CharField(blank=True, null=True, max_length=256, 
        help_text="An optional link which will be applied to the whole box.")
    
    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.template




class Page(models.Model):
    slug = models.SlugField(help_text="No spaces or special characters only dashes '-' and lowercase letters.")
    title = models.CharField(max_length=200,
        help_text="Title of the page - appears in the page.")
    meta_title = models.CharField(max_length=200, blank=True, null=True,
        help_text="A more verbose title useful for Google")
    meta_description = models.TextField(blank=True, null=True, 
        help_text="A description of the page useful for Google.")
    parent = models.ForeignKey('self', blank=True, null=True, 
        help_text="Is this the subpage of another?")
    content = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='images/learn', blank=True, null=True,
        help_text="Optional promo image for this page.")
    template = models.CharField(max_length=200, blank=True, null=True, 
        help_text="Leave this alone if you don't know what it does!")
    is_top_nav = models.BooleanField(default=False,
        help_text="Check this box if you want this page to appear in the main navigation")
    top_nav_position = models.IntegerField(default=0, blank=True, null=True,
        help_text="Which position should the item appear in the topnav (left-to-right, 0 is furthest left)")
    is_client_testimonial = models.BooleanField(default=False,
        help_text="Click this if the page is a client testimonial. It will appear in the footer if it is.")
    
    right_boxes = models.ManyToManyField(RightBox, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
        
    
    def get_root(self):
        def _iterator(obj):
            if obj.parent:
                return _iterator(obj.parent)
            else:
                return obj
        return _iterator(self)
    
    def get_boxes(self):
        boxes = self.right_boxes.all()
        if not self.right_boxes.all():
            boxes = self.get_root().right_boxes.all()
        html = ''
        print boxes
        for b in boxes:
            template = 'boxes/%s' % b.template
            x = render_to_string(template, {'box':b,})
            html = ''.join((html, x))
            
        return html
        
    
    def get_nav_tree(self):
        if self.parent is None: 
            nav_items = Page.objects.filter(parent=self)
        else:
            if self.parent.parent is None:
                nav_items = Page.objects.filter(parent=self.parent)
            else:
                if self.parent.parent.parent is None:
                    nav_items = Page.objects.filter(parent=self.parent.parent)
                else:
                    if self.parent.parent.parent.parent is None:
                        nav_items = Page.objects.filter(parent=self.parent.parent.parent)
        return nav_items
    
    def get_children(self):
        items = Page.objects.filter(parent=self)
        if len(items) < 1:
            return None
        else:
            return items
    
    def get_absolute_url(self):
        url = "/%s/" % self.slug  
        return url

