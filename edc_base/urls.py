from django.urls.conf import path

from edc_base.views import HomeView

app_name = 'edc_base'

urlpatterns = [
    # url(r'^jsreverse/$', urls_js, name='js_reverse'),
    #     path(r'accounts/login', LoginView.as_view(), name='login_url'),
    #     path(r'login', LoginView.as_view(), name='login_url'),
    #     path(r'logout', LogoutView.as_view(), name='logout_url'),
    #     path(r'settings/', RedirectView.as_view(url='/home/'), name='settings_url'),
    #     path(r'tz_detect/', include('tz_detect.urls')),
    path(r'', HomeView.as_view(), name='home_url'),
]
