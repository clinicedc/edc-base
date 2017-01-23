
class Fieldset:

    def __init__(self, *fields, section=None):
        self.fieldset = (section, {'fields': fields})

    def __call__(self):
        return self.fieldset
