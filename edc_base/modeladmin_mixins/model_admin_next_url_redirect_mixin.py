from django.urls import reverse

from .base_model_admin_redirect_mixin import BaseModelAdminRedirectMixin


class ModelAdminNextUrlRedirectMixin(BaseModelAdminRedirectMixin):

    """Redirect on add, change, delete by reversing a url_name
    in the querystring.

    In your url &next=my_url_name,arg1,arg2&agr1=value1&arg2=
    value2&arg3=value3&arg4=value4...etc.
    """

    querystring_name = 'next'

    def render_delete_form(self, request, context):
        return super().render_delete_form(request, context)

    def delete_view(self, request, object_id, extra_context=None):
        return super().delete_view(request, object_id, extra_context=extra_context)

    def redirect_url(self, request, obj, post_url_continue=None):
        kwargs = request.GET.dict()
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if kwargs.get(self.querystring_name):
            url_name = kwargs.get(self.querystring_name).split(',')[0]
            attrs = kwargs.get(self.querystring_name).split(',')[1:]
            kwargs = {k: kwargs.get(k) for k in attrs if kwargs.get(k)}
            redirect_url = reverse(url_name, kwargs=kwargs)
        return redirect_url
