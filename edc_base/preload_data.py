import sys

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.color import color_style
from django.db.models.deletion import ProtectedError

style = color_style()


class PreloadData:

    def __init__(self, list_data=None, model_data=None, unique_field_data=None):
        self.list_data = list_data or {}
        self.model_data = model_data or {}
        self.unique_field_data = unique_field_data or {}
        self.load_list_data()
        self.load_model_data()
        self.update_unique_field_data()

    def load_list_data(self):
        """Loads data into a list model.

        List models have short_name, name where short_name is the unique field.

        Format:
            {model_name1: [(short_name1, name), (short_name2, name),...],
             model_name1: [(short_name1, name), (short_name2, name),...],
            ...}
        """
        for model_name in self.list_data.keys():
            try:
                model = django_apps.get_model(model_name)
                for data in self.list_data.get(model_name):
                    short_name, display_value = data
                    try:
                        obj = model.objects.get(short_name=short_name)
                    except ObjectDoesNotExist:
                        model.objects.create(
                            short_name=short_name, name=display_value)
                    else:
                        obj.name = display_value
                        obj.save()
            except Exception as e:
                sys.stdout.write(style.ERROR(str(e) + '\n'))

    def load_model_data(self):
        """Loads dta into a model.

        Must have a unique field

        Format:
            {model_name1: {field_name1: value, field_name2: value ...},
             model_name2: {field_name1: value, field_name2: value ...},
             ...}
        """
        for model_name, data in self.model_data.items():
            model = django_apps.get_model(*model_name.split('.'))
            unique_field = self.get_unique_field(model)
            try:
                obj = model.objects.get(
                    **{unique_field: data.get(unique_field)})
            except model.DoesNotExist:
                model.objects.create(**data)
            else:
                for key, value in data.items():
                    setattr(obj, key, value)
                obj.save()

    def update_unique_field_data(self):
        """Updates the values of the unique fields in a model.

        Model must have a unique field and the record must exist

        Format:
            {model_name1: {unique_field_name: (current_value, new_value)},
             model_name2: {unique_field_name: (current_value, new_value)},
             ...}
        """
        for model_name, data in self.unique_field_data.items():
            model = django_apps.get_model(*model_name.split('.'))
            for field, values in data.items():
                try:
                    obj = model.objects.get(**{field: values[1]})
                except model.DoesNotExist as e:
                    try:
                        obj = model.objects.get(**{field: values[0]})
                    except model.DoesNotExist as e:
                        sys.stdout.write(style.ERROR(str(e) + '\n'))
                    except MultipleObjectsReturned as e:
                        sys.stdout.write(style.ERROR(str(e) + '\n'))
                    else:
                        setattr(obj, field, values[1])
                        obj.save()
                else:
                    try:
                        obj = model.objects.get(**{field: values[0]})
                    except model.DoesNotExist as e:
                        pass
                    else:
                        try:
                            obj.delete()
                        except ProtectedError:
                            pass

    def get_unique_field(self, model):
        """Returns the field name for the unique field.
        """
        unique_field = None
        for field in model._meta.get_fields():
            try:
                if field.unique and field.name != 'id':
                    unique_field = field.name
                    break
            except AttributeError:
                pass
        return unique_field
