from edc_model_admin import (
    AddressModelAdminMixin, ModelAdminChangelistButtonMixin, ModelAdminChangelistModelButtonMixin,
    LimitedAdminInlineMixin, StackedInlineMixin, TabularInlineMixin,
    FormAsJSONModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fields, audit_fieldset_tuple,
    ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin, ModelAdminInstitutionMixin,
    ModelAdminModelRedirectMixin, ModelAdminNextUrlRedirectMixin,
    ModelAdminReadOnlyMixin, ModelAdminRedirectOnDeleteMixin,
    ModelAdminNextUrlRedirectError)


from warnings import warn
warn('Import path edc_base.modeladmin_mixins is Deprecated and will be removed. '
     'Import from edc_model_admin instead.', DeprecationWarning, stacklevel=2)
