from django.conf import settings
from django.apps import apps as django_apps


def edc_base_startup(verbose=None):
    """Inspect all models to set edc specific attributes."""
    for app in settings.INSTALLED_APPS:
        if 'contrib' not in app:
            if '.' in app:
                app_label = app.split('.')[-1:][0]
            else:
                app_label = app
            try:
                for model in django_apps.get_models(django_apps.get_app_config(app_label)):
                    try:
                        get_model_if_tuple(model)
                        discover_visit_model_if_exists(model)
                    except AttributeError:
                        pass
            except LookupError:
                pass


def get_model_if_tuple(model):
    for attr in ['off_study_model', 'death_report_model']:
        try:
            app_label, model_name = getattr(model, attr)
            model_class = django_apps.get_model(app_label, model_name)
            setattr(model, attr, model_class or getattr(model, attr))
        except (TypeError, AttributeError, ValueError):
            pass


def discover_visit_model_if_exists(model):
    """Set model class attributes `visit_model`, `visit_model_attr` and `natural_key.dependencies`."""
    try:
        model.visit_model, model.visit_model_attr = _configure_visit_model_attrs(model)
        model.natural_key.dependencies = ['{}.{}'.format(
            model.visit_model._meta.app_label,
            model.visit_model._meta.model_name)]
    except AttributeError:
        pass


def _configure_visit_model_attrs(model):
    """Discover and return the visit_model and visit_model_attr from the model class."""
    visit_model, visit_model_attr = None, None
    for field in model._meta.fields:
        try:
            field.rel.to.visit_model_mixin
            visit_model = field.rel.to
            visit_model_attr = field.name
            break
        except AttributeError:
            pass
    try:
        if model.visit_model_attr:
            visit_model_attr = model.visit_model_attr
    except AttributeError:
        pass
    return visit_model, visit_model_attr


def _get_inline_parent_model(model):
    """Discover and return the visit_model and visit_model_attr from the model class."""
    return [fld for fld in model._meta.fields if fld.name == model.parent_model_attr][0].rel.to
