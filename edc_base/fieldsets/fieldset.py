
class Fieldset:

    """"A class to format a fieldset.

    If used as a callable returns a formatted fieldset"""

    def __init__(self, *fields, section=None):
        self.fieldset = (section, {'fields': fields})

    def __call__(self):
        """Returns a formatted fieldset."""
        return self.fieldset
