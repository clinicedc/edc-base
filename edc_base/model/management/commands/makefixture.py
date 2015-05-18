# http://djangosnippets.org/snippets/918/
#save into anyapp/management/commands/makefixture.py
#or back into django/core/management/commands/makefixture.py
#v0.1 -- current version
#known issues:
#no support for generic relations
#no support for one-to-one relations
import six

from optparse import make_option

from django.core import serializers
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import LabelCommand
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related import ManyToManyField
from django.db.models.loading import get_models

DEBUG = False


def model_name(m):
    module = m.__module__.split('.')[:-1]  # remove .models
    return ".".join(module + [m._meta.object_name])


class Command(LabelCommand):
    """
    "Make fixture" command. Highly useful for making test fixtures. Use it to pick only few items from your data to serialize, restricted by primary keys. By default command also serializes foreign keys and m2m relations. You can turn off related items serialization with --skip-related option.

    How to use::

        python manage.py makefixture

    will display what models are installed::

        python manage.py makefixture User[:3]

    or::

        python manage.py makefixture auth.User[:3]

    or::

        python manage.py makefixture django.contrib.auth.User[:3]

    will serialize users with ids 1 and 2, with assigned groups, permissions and content types.::

        python manage.py makefixture YourModel[3] YourModel[6:10]

    will serialize YourModel with key 3 and keys 6 to 9 inclusively.Of course, you can serialize
    whole tables, and also different tables at once, and use options of dumpdata::

        python manage.py makefixture --format=xml --indent=4 YourModel[3] AnotherModel auth.User[:5] auth.Group
    """

    help = 'Output the contents of the database as a fixture of the given format.'
    args = 'modelname[pk] or modelname[id1:id2] repeated one or more times'
    option_list = BaseCommand.option_list + (
        make_option('--skip-related', default=True, action='store_false', dest='propagate',
            help='Specifies if we shall not add related objects.'),
        make_option('--format', default='json', dest='format',
            help='Specifies the output serialization format for fixtures.'),
        make_option('--indent', default=None, dest='indent', type='int',
            help='Specifies the indent level to use when pretty-printing output'),
    )

    def handle_models(self, models, **options):
        format = options.get('format', 'json')
        indent = options.get('indent', None)
        show_traceback = options.get('traceback', False)
        propagate = options.get('propagate', True)

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in serializers.get_public_serializer_formats():
            raise CommandError("Unknown serialization format: %s" % format)

        try:
            serializers.get_serializer(format)
        except KeyError:
            raise CommandError("Unknown serialization format: %s" % format)

        objects = []
        for model, slice in models:
            if isinstance(slice, six.string_types):
                objects.extend(model._default_manager.filter(pk__exact=slice))
            elif not slice or type(slice) is list:
                items = model._default_manager.all()
                if slice and slice[0]:
                    items = items.filter(pk__gte=slice[0])
                if slice and slice[1]:
                    items = items.filter(pk__lt=slice[1])
                items = items.order_by(model._meta.pk.attname)
                objects.extend(items)
            else:
                raise CommandError("Wrong slice: %s" % slice)

        all = objects
        if propagate:
            collected = set([(x.__class__, x.pk) for x in all]) 
            while objects:
                related = []
                for x in objects:
                    if DEBUG:
                        print "Adding %s[%s]" % (model_name(x), x.pk)
                    for f in x.__class__._meta.fields + x.__class__._meta.many_to_many:
                        if isinstance(f, ForeignKey):
                            new = getattr(x, f.name) # instantiate object
                            if new and not (new.__class__, new.pk) in collected:
                                collected.add((new.__class__, new.pk))
                                related.append(new)
                        if isinstance(f, ManyToManyField):
                            for new in getattr(x, f.name).all():
                                if new and not (new.__class__, new.pk) in collected:
                                    collected.add((new.__class__, new.pk))
                                    related.append(new)
                objects = related
                all.extend(objects)

        try:
            return serializers.serialize(format, all, indent=indent)
        except Exception, e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)

    def get_models(self):
        return [(m, model_name(m)) for m in get_models()]

    def handle_label(self, labels, **options):
        parsed = []
        for label in labels:
            search, pks = label, ''
            if '[' in label:
                search, pks = label.split('[', 1)
            slice = ''
            if ':' in pks: 
                slice = pks.rstrip(']').split(':', 1)
            elif pks: 
                slice = pks.rstrip(']')
            models = [model for model, name in self.get_models()
                            if name.endswith('.' + search) or name == search]
            if not models:
                raise CommandError("Wrong model: %s" % search)
            if len(models) > 1:
                raise CommandError("Ambiguous model name: %s" % search)
            parsed.append((models[0], slice))
        return self.handle_models(parsed, **options)

    def list_models(self):
        names = [name for _model, name in self.get_models()]
        raise CommandError('Neither model name nor slice given. Installed model names: \n%s' % ",\n".join(names))

    def handle(self, *labels, **options):
        if not labels:
            self.list_models()

        output = []
        label_output = self.handle_label(labels, **options)
        if label_output:
                output.append(label_output)
        return '\n'.join(output)
