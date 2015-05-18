from django.db.models import get_models
from django.core.management.base import LabelCommand
from django.db import connection, transaction

from edc.base.model.models import BaseUuidModel


class Command(LabelCommand):

    help = 'Verify all BaseUuidModel subclasses have the required revision field.'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        for model in get_models():
            if issubclass(model, BaseUuidModel):
                table_name = model._meta.__dict__.get('db_table')
                print 'checking {0}'.format(table_name)
                try:
                    cursor.execute("ALTER TABLE {0} add column `revision` varchar(50)".format(table_name))
                    transaction.commit_unless_managed()
                    print '**Altered table {0}'.format(table_name)
                except:
                    pass
