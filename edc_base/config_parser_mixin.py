import os
import sys

import configparser

from django.conf import settings
from django.core.management.color import color_style
from django.core.exceptions import ImproperlyConfigured

style = color_style()


class ConfigParserMixin:

    config_filename = 'default_config.ini'
    config_folder = os.path.join(settings.BASE_DIR.ancestor(1), 'etc')
    default_config = {}

    @property
    def config_section(self):
        """Return the config section name."""
        try:
            return self.name  # from AppConfig
        except AttributeError:
            raise AttributeError(
                'Attribute \'config_section\' expects \'name\' attribute. If not mixing with AppConfig, '
                'set attribute \'config_section\' manually.')

    def create_config_file(self, name=None):
        """Create a default ini file if one does not already exist."""
        config_path = os.path.join(settings.BASE_DIR.ancestor(1), 'etc', self.config_filename)
        if not os.path.exists(os.path.join(config_path)):
            sys.stdout.write(style.NOTICE(
                'Warning: Creating default configuration file \'{}\'. See {}.AppConfig\n'.format(config_path, self.config_section)))
            config = configparser.ConfigParser()
            config[self.config_section] = self.default_config
            try:
                with open(config_path, 'w') as f:
                    config.write(f)
            except FileNotFoundError:
                raise ImproperlyConfigured(
                    'Unable to create config file {}. Does config folder exist?. '
                    'See {}.AppConfig and edc_base.AppConfig'.format(config_path, self.config_section_name))

    def get_config(self, name=None):
        """Return the config for this section (app_config.name)."""
        self.create_config_file()
        config = configparser.ConfigParser()
        sys.stdout.write(
            ' Reading configuration file \'{}\'.\n'.format(self.config_filename))
        config.read(os.path.join(self.config_folder, self.config_filename))
        return config[self.config_section]

    def set_config_attrs(self, name=None):
        """Set configuration keys as attributes on the class."""
        name = name or self.config_section
        config = self.get_config(name)
        for k, v in config.items():
            setattr(self, k, v)
