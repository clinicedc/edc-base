from edc_base.model.validators import TelephoneNumber


def BWCellNumber(value):
    TelephoneNumber(value, '^[7]{1}[12345678]{1}[0-9]{6}$', 'cell')


def BWTelephoneNumber(value):
    TelephoneNumber(value, '^[2-8]{1}[0-9]{6}$', 'telephone')
