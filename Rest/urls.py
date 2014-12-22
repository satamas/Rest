from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

admin.autodiscover()

from rest import urls as rest_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Rest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(rest_urls)),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
