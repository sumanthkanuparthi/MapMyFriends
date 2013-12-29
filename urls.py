from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls')),
    url(r'^canvas/TOS', 'hellodjango.views.tos'),
    url(r'^canvas/privacy-policy', 'hellodjango.views.pp'),
    url(r'^canvas/user-support', 'hellodjango.views.usupp'),
    url(r'^canvas/', 'hellodjango.views.home'),
)
