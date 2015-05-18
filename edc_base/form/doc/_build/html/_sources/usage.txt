Usage
=====

The :func:`logic` method simplifies coding in the :file:`forms.py` for "skip" logic so that you don't need to write all the if/else statements.

In this example, field `has_ga` is a yes/no question that if answered 'YES' requires that you complete 
question 'ga' and if 'NO' that you don't.

.. code-block:: python
   :emphasize-lines: 5

    class MaternalLabDelForm (BaseMaternalModelForm):
        
        def clean(self):
            cleaned_data = self.cleaned_data
            self.logic.test(cleaned_data, 'has_ga', 'YES', 'ga')
    
        class Meta:
            model = MaternalLabDel
            
See :mod:`classes` for more options.