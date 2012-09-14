from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse



from tinymce import models as tinymce_models



class HomePage(models.Model):
    is_active = models.BooleanField(default=True)
    identifier = models.CharField(max_length=200, null=True, blank=True,
        help_text="A name you give the homepage to remind you which one it is!")
    
    intro_box_1 = tinymce_models.HTMLField(help_text="Use Heading3 and Paragraph only!")
    intro_box_1_page = models.ForeignKey('Page', related_name="intro_box_1")
    intro_box_1_text = models.CharField(max_length=200)
    
    intro_box_2 = tinymce_models.HTMLField()
    intro_box_2_page = models.ForeignKey('Page', related_name="intro_box_2")
    intro_box_2_text = models.CharField(max_length=200)
    
    intro_box_3 = tinymce_models.HTMLField()
    intro_box_3_page = models.ForeignKey('Page', related_name="intro_box_3")
    intro_box_3_text = models.CharField(max_length=200)
    
    twin_box_1 = tinymce_models.HTMLField(null=True, blank=True)
    twin_box_2 = tinymce_models.HTMLField(null=True, blank=True)
    
    long_box = tinymce_models.HTMLField(null=True, blank=True)
    
    image_promo_image = models.ImageField(upload_to='images/promo')
    image_promo_text = models.CharField(max_length=200)
    image_promo_page = models.ForeignKey('Page', related_name="image_promo_text")
    image_promo_link = models.URLField(null=True, blank=True)
    
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES)
    
    def __unicode__(self):
        return self.identifier
        
       

class News(models.Model):
    date_posted = models.DateTimeField()
    slug = models.SlugField()
    title = models.CharField(max_length=256)
    summary = models.TextField()
    text = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='images/news', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        url = reverse('news', args=[self.slug])
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
        return items
    
    def get_absolute_url(self):
        url = "/%s/" % self.slug  
        return url

    def get_products_mentioned(self):
        teas = Product.objects.filter(is_active=True)
        products = []
        for tea in teas:
            if tea.name in self.content:
                products.append(tea)
        return products