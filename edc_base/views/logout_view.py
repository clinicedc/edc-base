from django.contrib.auth.views import logout
from django.views.generic import RedirectView


class LogoutView(RedirectView):

    permanent = True
    pattern_name = 'login_url'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
