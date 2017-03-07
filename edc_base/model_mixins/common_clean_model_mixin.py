from django.db import models


class CommonCleanModelMixin(models.Model):
    """A mixin that adds a method for validation logic that can be shared with a form
    when the form is declared using the CommonCleanModelFormMixin."""

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            self.common_clean()
        super().save(*args, **kwargs)

    def common_clean(self):
        """A method that can be shared between form clean and model.save."""
        pass

    @property
    def common_clean_exceptions(self):
        """A list of exceptions classes that are raised in the common_clean
        method for this class.

        The list is used by the form clean method. Any exception listed here will
        be re-raised as a forms.ValidationError."""
        return []

    class Meta:
        abstract = True
