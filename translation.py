from modeltranslation.translator import translator, TranslationOptions
from website.models import *

class PageTranslationOptions(TranslationOptions):
    fields = ('slug', 'title', 'meta_description', 'meta_title', 'content')
    
class NewsTranslationOptions(TranslationOptions):
    fields = ('slug', 'title', 'summary')

class RightBoxTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'link',)

translator.register(News, NewsTranslationOptions)
translator.register(Page, PageTranslationOptions)
translator.register(RightBox, RightBoxTranslationOptions)


