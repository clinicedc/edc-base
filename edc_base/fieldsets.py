import copy

from collections import OrderedDict


class FieldsetError(Exception):
    pass


class Fieldset:

    def __init__(self, *fields, section=None):
        self.fieldset = (section, {'fields': fields})

    def __call__(self):
        return self.fieldset


class Fieldsets:

    def __init__(self, fieldsets=None, **kwargs):
        self.fieldsets_asdict = OrderedDict(copy.deepcopy(fieldsets))

    @property
    def fieldsets(self):
        return tuple([(k, v) for k, v in self.fieldsets_asdict.items()])

    def add_fieldset(self, section=None, fields=None, fieldset=None):
        if fieldset:
            section = fieldset()[0]
            fields = fieldset()[1]['fields']
        self.fieldsets_asdict.update({section: {'fields': fields}})

    def insert_fields(self, *insert_fields, field_after=None, section=None):
        """Inserts fields after field_after in the given section."""
        fields = self._copy_section_fields(section)
        position = self._get_field_position(fields, field_after)
        for index, field in enumerate(insert_fields):
            fields.insert(index + position, field)
        self.fieldsets_asdict[section]['fields'] = tuple(fields)

    def remove_fields(self, *remove_fields, section=None):
        fields = self._copy_section_fields(section)
        fields = [f for f in fields if f not in remove_fields]
        self.fieldsets_asdict[section]['fields'] = tuple(fields)

    def _copy_section_fields(self, section):
        """Returns fields as a list which is a copy of the fields tuple in a
        section or raises if section does not exist."""
        try:
            fields = copy.copy(
                self.fieldsets_asdict[section]['fields'])
        except KeyError:
            raise FieldsetError(
                'Invalid fieldset section. Got {}'.format(section))
        return list(fields)

    def _get_field_position(self, fields, field_after):
        try:
            position = fields.index(field_after) + 1
        except ValueError:
            raise FieldsetError(
                'Field does not exist in section {}. Got {}'.format(
                    field_after))
        return position
