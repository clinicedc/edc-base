from edc_constants.constants import NOT_APPLICABLE, OPEN, CLOSED

DATE_ESTIMATED_NA = (
    (NOT_APPLICABLE, 'Not applicable'),
    ('not_estimated', 'No.'),
    ('D', 'Yes, estimated the Day'),
    ('MD', 'Yes, estimated Month and Day'),
    ('YMD', 'Yes, estimated Year, Month and Day'),
)

DATE_ESTIMATED = (
    ('-', 'No'),
    ('D', 'Yes, estimated the Day'),
    ('MD', 'Yes, estimated Month and Day'),
    ('YMD', 'Yes, estimated Year, Month and Day'),
)

IDENTITY_TYPE = (
    ('OMANG', 'Omang'),
    ('DRIVERS', 'Driver\'s License'),
    ('PASSPORT', 'Passport'),
    ('OMANG_RCPT', 'Omang Receipt'),
    ('OTHER', 'Other'),
)


REPORT_STATUS = (
    (OPEN, 'Open. Some information is still pending.'),
    (CLOSED, 'Closed. This report is complete'),
)
