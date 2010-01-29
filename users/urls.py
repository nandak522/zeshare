from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
    (r'^$', 'view_all_users', {'all_users_template':'all_users.html'}, 'all_users'),
    (r'^(?P<user_id>\d+)/(?P<user_slug_name>[\w-]+)/$', 'view_userprofile', {'userprofile_template':'user_profile.html'}, 'user_profile'),
)