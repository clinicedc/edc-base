import os
import sys

import configparser

from django.conf import settings
from django.core.management.color import color_style
from django.core.exceptions import ImproperlyConfigured

style = color_style()


class ConfigParserMixin:
    """Set AppConfig attributes via a text/ini configuration file."""

    config_filename = 'config.ini'
    config_items = {}
    _config_folder = None

    @property
    def config_folder(self):
        if not self._config_folder:
            try:
                self._config_folder = settings.ETC_DIR
            except AttributeError:
                self._config_folder = os.path.join(settings.BASE_DIR, 'etc')
                sys.stdout.write(style.NOTICE(
                    ' Warning: missing settings.ETC_DIR, using default configuration folder '
                    '\'{}\'\n'.format(self._config_folder)))
        return self._config_folder

    @property
    def config_path(self):
        return os.path.join(self.config_folder, self.config_filename)

    @property
    def config_section(self):
        """Return the config section name."""
        return self.name  # expected from AppConfig

    def create_config_file(self, name=None):
        """Create a default ini file if one does not already exist."""
        name = name or self.config_section
        if not os.path.exists(os.path.join(self.config_path)):
            sys.stdout.write(style.NOTICE(
                ' Note: Creating default configuration file \'{}\'. '
                'See {}.AppConfig\n'.format(self.config_path, name)))
        self.update_config_attrs(name)

    def get_config(self, name=None):
        """Return the config for this section (app_config.name)."""
        name = name or self.config_section
        self.create_config_file()
        config = configparser.ConfigParser()
        sys.stdout.write(
            ' Reading configuration file \'{}\'.\n'.format(self.config_filename))
        config.read(os.path.join(self.config_folder, self.config_filename))
        return config[name]

    def set_config_attrs(self, name=None):
        """Set configuration keys as attributes on the class."""
        name = name or self.config_section
        config = self.get_config(name)
        for k, v in config.items():
            setattr(self, k, v)

    def update_config_attrs(self, name=None):
        """Update ini file with config_items dict."""
        name = name or self.config_section
        config = configparser.ConfigParser()
        config[name] = self.config_items
        try:
            with open(self.config_path, 'w') as f:
                config.write(f)
        except FileNotFoundError:
            raise ImproperlyConfigured(
                'Unable to create config file {}. Does config folder exist?. '
                'See {}.AppConfig and edc_base.AppConfig'.format(self.config_path, name))
