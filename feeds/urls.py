from django.conf.urls.defaults import *
from feeds.views import LatestSnippets

feeds = {'snippets': LatestSnippets}

urlpatterns = patterns('',
    (r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, 'feeds'),
)