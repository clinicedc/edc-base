from ..model.models import BaseListModel


class TestM2m(BaseListModel):

    class Meta:
        app_label = 'edc_base'


class TestForeignKey(BaseListModel):

    class Meta:
        app_label = 'edc_base'
