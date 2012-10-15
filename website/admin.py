
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from website.models import *


class PageAdmin(TranslationAdmin):
    class Media:
        js = (
            '/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/modeltranslation/css/tabbed_translation_fields.css',),
        }

class RightBoxAdmin(TranslationAdmin):
    exclude = ('template',)
    class Media:
        js = (
            '/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/modeltranslation/css/tabbed_translation_fields.css',),
        }


class NewsAdmin(TranslationAdmin):
    exclude = ('text', 'image',)
    class Media:
        js = (
            '/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Page, PageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(HomePage)
admin.site.register(RightBox, RightBoxAdmin)

