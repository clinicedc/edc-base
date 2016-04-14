from datetime import datetime, time


def get_age_in_days(reference_date, dob):
    # convert dob to datetime, assume born midnight
    dob = datetime.combine(dob, time())
    # get timedelta
    tdelta = reference_date - dob
    # ...for age in days
    return tdelta.days
