[![Build Status](https://travis-ci.org/botswana-harvard/edc-base.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-base)
[![Coverage Status](https://coveralls.io/repos/botswana-harvard/edc-base/badge.svg?branch=develop&service=github)](https://coveralls.io/github/botswana-harvard/edc-base?branch=develop)
# edc-base

Base model, manager, field, validator, form and admin classes for Edc. 


Installation
------------

In the __settings__ file add:

	STUDY_OPEN_DATETIME = datetime.today()
	STUDY_CLOSE_DATETIME = datetime.today()

Optional __settings__ attributes:

	# phone number validtors
	# the default is '^[0-9+\(\)#\.\s\/ext-]+$'
	TELEPHONE_REGEX = '^[2-8]{1}[0-9]{6}$'
	CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$',
	

Audit trail (HistoricalRecord):
-------------------------------

HistoricalRecord is an almost identical version of `simple_history.models.HistoricalRecord`
with the exception of two methods:  `get_extra_fields()` and `add_extra_methods()`. Method 
`get_extra_fields()` method is overridden to change the *history_id* primary key from an 
`IntegerField` to a `UUIDField` so that it can work with edc-sync. Method `add_extra_methods()`
is overridden to add the methods from `edc_sync.mixins.SyncMixin` if module `edc_sync` is 
in INSTALLED_APP.


	from edc_base.model.models import HistoricalRecord
	from edc_sync.mixins import SyncMixin
	
	class MyModel(SyncMixin, BaseUuidModel):
		
		...
		history = HistoricalRecord()
		
		class Meta:
			app_label = 'my_app' 	

The audit trail models created by `simple_history` have a foreign key to `auth.User`.
In order for the models to work with `edc_sync` specify the edc_sync User model in settings:
	
	AUTH_USER_MODEL = 'edc_sync.User' 


Notes
-----

User created and modified fields behave as follows:
* created is only set on pre-save add
* modified is always updated
