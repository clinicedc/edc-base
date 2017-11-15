from django.urls import reverse, NoReverseMatch

from .base_model_admin_redirect_mixin import BaseModelAdminRedirectMixin


class ModelAdminNextUrlRedirectError(Exception):
    pass


class ModelAdminNextUrlRedirectMixin(BaseModelAdminRedirectMixin):

    """Redirect on add, change, delete by reversing a url_name
    in the querystring.

    In your url &next=my_url_name,arg1,arg2&agr1=value1&arg2=
    value2&arg3=value3&arg4=value4...etc.
    """

    def render_delete_form(self, request, context):
        return super().render_delete_form(request, context)

    def delete_view(self, request, object_id, extra_context=None):
        return super().delete_view(request, object_id, extra_context=extra_context)

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url
