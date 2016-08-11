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
    config_attrs = {}
    _config_folder = None

    def overwrite_config_attrs_on_class(self, section=None):
        """Read config file and overwrite attributes on the class."""
        config = configparser.ConfigParser()
        config_attrs = {section: self.config_attrs[section]} if section else self.config_attrs
        sys.stdout.write(
            ' * reading configuration file \'{}\'.\n'.format(self.config_filename))
        config.read(os.path.join(self.config_folder, self.config_filename))
        for section, attrs in config_attrs.items():
            if section not in config.sections():
                self.write_default_config(section)
                config.read(os.path.join(self.config_folder, self.config_filename))
            sys.stdout.write(
                ' * overwriting {} config for {}.\n'.format(section, ', '.join([self.convert_attr(attr)[0] for attr in attrs])))
            for attr in attrs:
                attr, value = self.to_python(attr, section, config)
                setattr(self, attr, value or None)

    def convert_attr(self, attr):
        try:
            attr, datatype = attr
        except ValueError:
            attr, datatype = attr, None
        return attr, datatype

    def to_python(self, attr, section, config):
        """Return attr, value where value is converted back to a python object."""
        attr, datatype = self.convert_attr(attr)
        if datatype in (list, tuple):
            value = config[section][attr]
            if value:
                value = tuple(''.join(value.split()).split(','))
        elif datatype == bool:
            value = config[section].getboolean(attr)
        else:
            value = config[section].get(attr)
        return attr, value

    def get_prep_value(self, attr, section, config):
        """Return attr, value where value is prepared for the write to file."""
        attr, datatype = self.convert_attr(attr)
        try:
            value = getattr(self, attr)
            if not value:
                value = ''
            elif datatype in (list, tuple):
                value = ','.join(value)
        except AttributeError:
            value = ''
        return attr, value

    def write_default_config(self, section):
        """Write the config file with default values and return the config instance."""
        config = configparser.ConfigParser()
        values = {}
        for attr in self.config_attrs[section]:
            attr, value = self.get_prep_value(attr, section, config)
            values[attr] = value
        config[section] = values
        try:
            sys.stdout.write(style.NOTICE(
                ' * writing default configuration for \'{}\'.\n'.format(section)))
            with open(self.config_path, 'a') as f:
                config.write(f)
        except FileNotFoundError:
            raise ImproperlyConfigured(
                'Unable to create config file {}. Does config folder exist?. '
                'See {}.AppConfig and edc_base.AppConfig'.format(self.config_path, section))

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
