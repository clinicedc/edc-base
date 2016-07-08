from django.conf import settings
try:
    from django.db.models import loading as apps
except:
    from django.apps import apps

def edc_base_startup(verbose=None):
    """Inspect all models to set edc specific attributes."""
    for app_str in settings.INSTALLED_APPS:
        if 'contrib' not in app_str:
            if '.' in app_str:
                app_str = app_str.split('.')[-1:][0]
            try:
                for model in apps.get_models(apps.get_app_config(app_str)):
                    try:
                        _get_model_if_tuple(model)
                        _discover_visit_model_if_exists(model)
                    except AttributeError:
                        pass
            except LookupError:
                pass

def _get_model_if_tuple(model):
    for attr in ['off_study_model', 'death_report_model']:
        try:
            app_label, model_name = getattr(model, attr)
            model_class = apps.get_model(app_label, model_name)
            setattr(model, attr, model_class or getattr(model, attr))
        except (TypeError, AttributeError, ValueError):
            pass


def _discover_visit_model_if_exists(model):
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
