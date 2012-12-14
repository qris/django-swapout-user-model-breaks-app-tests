DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(os.path.dirname(__file__), 'school.db'),
		'HOST': '',
		'USER': '',
		'PASSWORD': '',
		'PORT': '',
	},
	'website': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(os.path.dirname(__file__), 'website.db'),
		'HOST': '',
		'USER': '',
		'PASSWORD': '',
		'PORT': '',
	},
	'license': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(os.path.dirname(__file__), 'license.db'),
		'HOST': '',
		'USER': '',
		'PASSWORD': '',
		'PORT': '',
	},
	'tle': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(os.path.dirname(__file__), 'tle.db'),
		'HOST': '',
		'USER': '',
		'PASSWORD': '',
		'PORT': '',
	},
}

EMAIL_HOST = 'localhost'

