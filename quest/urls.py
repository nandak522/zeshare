from django.conf.urls.defaults import *

urlpatterns = patterns('quest.views',
    (r'^$', 'view_all_snippets', {'all_snippets_template':'all_snippets.html'}, 'all_snippets'),
    (r'^recent/$', 'view_recent_snippets', {'recent_snippets_template':'recent_snippets.html'}, 'recent_snippets'),
    (r'^popular/$', 'view_popular_snippets', {'popular_snippets_template':'popular_snippets.html'}, 'popular_snippets'),
    (r'^(?P<snippet_id>\d+)/(?P<snippet_slug>[\w-]+)/$', 'view_snippet_profile', {'snippet_profile_template':'snippet_profile.html'}, 'snippet_profile'),
    (r'^add/$', 'view_add_snippet', {'add_snippet_template':'add_snippet.html', 'snippet_profile_template':'snippet_profile.html'}, 'add_snippet')
)