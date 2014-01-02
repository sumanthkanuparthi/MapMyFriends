from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^canvas/map','hellodjango.views.map'),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls')),
    url(r'^canvas/TOS', 'hellodjango.views.tos'),
    url(r'^canvas/privacy-policy', 'hellodjango.views.pp'),
    url(r'^canvas/user-support', 'hellodjango.views.usupp'),
    url(r'^canvas/rev_geocode', 'hellodjango.views.rev_geocode'),
    url(r'^canvas/friends/(?P<city>[\w|\W]+)', 'hellodjango.views.friend_list'),
    url(r'^canvas/', 'hellodjango.views.home'),
)
