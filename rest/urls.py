from django.conf.urls import url, patterns
from django.views.decorators.csrf import csrf_exempt

from rest.views import CustomersView, ComplainView, ComplainSelectAllView, CustomerSelectAllView, \
    ComplainSelectByUserView, ComplainSelectByTimeAndUserView, ComplainSelectByTimeView


__author__ = 'atamas'

urlpatterns = patterns(
    'rest.views',
    # Examples:
    # url(r'^$', 'Rest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^customer/?$', csrf_exempt(CustomersView.as_view())),
    url(r'^complain/?$', csrf_exempt(ComplainView.as_view())),
    url(r'^complain/select/date/?$', csrf_exempt(ComplainSelectByTimeView.as_view())),
    url(r'^complain/select/date/customer/?$', csrf_exempt(ComplainSelectByTimeAndUserView.as_view())),
    url(r'^complain/select/customer/?$', csrf_exempt(ComplainSelectByUserView.as_view())),
    url(r'^complain/select/all/?$', csrf_exempt(ComplainSelectAllView.as_view())),
    url(r'^customer/select/all/?$', csrf_exempt(CustomerSelectAllView.as_view())),
    url(r'', csrf_exempt(ComplainSelectAllView.as_view())),
)
