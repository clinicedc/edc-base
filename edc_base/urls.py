from django.conf.urls import url
from edc_base.views import LoginView, LogoutView

"""
Add to your app as

[
   ...
    url(r'home/', HomeView.as_view(), name='home_url'),  # your home view, needed by base.html
    url(r'', include('edc_base.urls')),  # login, logout
]

"""
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'accounts/login', LoginView.as_view(), name='login_url'),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(), name='logout_url'),
    url(r'', RedirectView.as_view(url='/home/'), name='home'),
]
