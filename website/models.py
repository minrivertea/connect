from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse



from tinymce import models as tinymce_models



class HomePage(models.Model):
    is_active = models.BooleanField(default=True)
    identifier = models.CharField(max_length=200, null=True, blank=True, default="homepage",
        help_text="An optional name you give the homepage to remind you which one it is!")
    
    logo_tagline = models.CharField(max_length=200, blank=True, null=True)
    
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
    
    
    google_analytics = models.TextField(help_text="The code snippet from Google Analytics used to track your customers. Include the <script> tags please!",
        blank=True, null=True)
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES,
        help_text="Which language is this variation of the homepage?")
    
    def __unicode__(self):
        return self.identifier
        
       

class News(models.Model):
    date_posted = models.DateTimeField(help_text="Set this to a date in the future to do scheduled posting of news.")
    slug = models.SlugField(help_text="The URL of the page - only dashes and lowercase a-z characters please!")
    title = models.CharField(max_length=256, help_text="Name of the news item.")
    summary = models.TextField(help_text="A short summary of the item (appears in listings)")
    text = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='images/news', blank=True, null=True,
        help_text="An optional image; larger than 200px wide please!")
    is_published = models.BooleanField(default=False,
        help_text="Uncheck this to remove item from the website but continue editing (draft).")
    
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        url = reverse('news_item', args=[self.slug])
        return url


PROJECT = 'project.html'
CONTACT = 'contact.html'
SOCIAL = 'social.html'
RIGHT_BOXES = (
    (PROJECT, u"Project"),
    (SOCIAL, u"Social"),
    (CONTACT, u"Contact Us"),
)


class RightBox(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    template = models.CharField(max_length=200, choices=RIGHT_BOXES)
    content = tinymce_models.HTMLField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/right-boxes")
    link = models.CharField(blank=True, null=True, max_length=256)
    
    def __unicode__(self):
        return self.title




class Page(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    content = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='images/learn', blank=True, null=True)
    template = models.CharField(max_length=200, blank=True, null=True, 
        help_text="Leave this alone if you don't know what it does!")
    is_top_nav = models.BooleanField(default=False)
    top_nav_position = models.IntegerField(default=0, blank=True, null=True)
    is_client_testimonial = models.BooleanField(default=False)
    
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
        #boxes = self.boxes
        #if not self.boxes:
        #    boxes = self.get_root.boxes
        boxes = RightBox.objects.exclude(title=None, link=None, content=None)
        
        html = []
        for b in boxes:
            template = 'boxes/%s' % b.template
            x = render_to_string(template, {'box':b,})
            html.append(x)
            
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

