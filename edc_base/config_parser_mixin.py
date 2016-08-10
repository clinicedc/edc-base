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
    config_attrs = []
    _config_folder = None

    def overwrite_config_attrs_on_class(self, config_section):
        """Read config file and overwrite attributes on the class."""
        config = self.read_config_file(config_section)
        sys.stdout.write(
            ' * overwriting config for {}.\n'.format(', '.join(self.config_attrs)))
        for k in self.config_attrs:
            setattr(self, k, config[config_section][k])

    def read_config_file(self, config_section):
        """Read the config file and return the config instance."""
        config = configparser.ConfigParser()
        sys.stdout.write(
            ' * reading configuration file \'{}\'.\n'.format(self.config_filename))
        config.read(os.path.join(self.config_folder, self.config_filename))
        try:
            config[config_section]
        except KeyError:
            config = self.write_config_file(config_section)
        return config

    def write_config_file(self, config_section):
        """Write the config file with default values and return the config instance."""
        config = configparser.ConfigParser()
        items = {}
        for k in self.config_attrs:
            try:
                value = getattr(self, k)
            except AttributeError:
                value = ''
            items[k] = value
        config[config_section] = items
        try:
            sys.stdout.write(style.NOTICE(
                ' Note: Creating default configuration file \'{}\'. '
                'See {}.AppConfig\n'.format(self.config_path, config_section)))
            with open(self.config_path, 'a') as f:
                config.write(f)
        except FileNotFoundError:
            raise ImproperlyConfigured(
                'Unable to create config file {}. Does config folder exist?. '
                'See {}.AppConfig and edc_base.AppConfig'.format(self.config_path, config_section))
        return config

    @property
    def config_folder(self):
        """Return the projects ETC folder."""
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
