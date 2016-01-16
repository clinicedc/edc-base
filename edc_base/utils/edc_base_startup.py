from django.db.models.loading import get_apps, get_models, get_model


def edc_base_startup(verbose=None):
    """Inspect all models to set edc specific attributes."""
    for app in get_apps():
        for model in get_models(app):
            try:
                _get_model_if_tuple(model)
                _discover_visit_model_if_exists(model)
            except AttributeError:
                pass


def _get_model_if_tuple(model):
    for attr in ['off_study_model', 'death_report_model']:
        try:
            app_label, model_name = getattr(model, attr)
            model_class = get_model(app_label, model_name)
            setattr(model, attr, model_class or getattr(model, attr))
        except (TypeError, AttributeError, ValueError):
            pass


def _discover_visit_model_if_exists(model):
    try:
        model.visit_model, model.visit_model_attr = _configure_visit_model_attrs(model)
        try:
            model.get_visit = lambda self: getattr(self, model.visit_model_attr)
        except TypeError as e:
            raise TypeError(e, 'Specify the visit_model_attr on {}'.format(model))
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
