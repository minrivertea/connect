from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views


urlpatterns = patterns('',
    url(r'^$', views.index, name="home"),
    url(r'^news/(?P<slug>[\w-]+)/$', views.news_item, name="news_item"),
)
