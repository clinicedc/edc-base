from django.apps import apps as django_apps


class NavbarItem:

    def __init__(self, name=None, app_config_name=None, app_config_attr=None,
                 label=None, title=None, html_id=None, fa_icon=None, **kwargs):
        self._url_name = None
        self._app_config = None
        self.app_config_name = app_config_name
        self.app_config_attr = app_config_attr or 'default_url_name'
        self.name = name or app_config_name
        self.label = label or app_config_name
        self.title = title or self.label
        self.html_id = html_id or label
        self.fa_icon = fa_icon
        self.kwargs = kwargs

    def __repr__(self):
        return '{0}(<name={1.name}, app_config_name={1.app_config_name}, ...>)'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{}, {}'.format(self.name, self.label)

    @property
    def url_name(self):
        if not self._url_name:
            self._url_name = getattr(self.app_config, self.app_config_attr)
        return self._url_name

    @property
    def app_config(self):
        if not self._app_config:
            self._app_config = django_apps.get_app_config(self.app_config_name)
        return self._app_config
