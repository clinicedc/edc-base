from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from edc_base.views import LoginView, LogoutView

app_name = 'edc_base'

urlpatterns = [
    # url(r'^jsreverse/$', urls_js, name='js_reverse'),
    url(r'accounts/login', LoginView.as_view(), name='login_url'),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(), name='logout_url'),
    url(r'settings/', RedirectView.as_view(url='/home/'), name='settings_url'),
    url(r'^tz_detect/', include('tz_detect.urls')),
]
