[![Build Status](https://travis-ci.org/botswana-harvard/edc-base.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-base)
[![PyPI version](https://badge.fury.io/py/edc-base.svg)](http://badge.fury.io/py/edc-base)
# edc-base

Base model, manager, field, validator, form and admin classes for Edc. 


Installation
------------

	pip install edc-base

In the __settings__ file add:

	STUDY_OPEN_DATETIME = datetime.today()
	STUDY_CLOSE_DATETIME = datetime.today()

Optional __settings__ attributes:

	# phone number validtors
	# the default is '^[0-9+\(\)#\.\s\/ext-]+$'
	TELEPHONE_REGEX = '^[2-8]{1}[0-9]{6}$'
	CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$',
	