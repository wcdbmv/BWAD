from backend.settings import *

INSTALLED_APPS.append('readonly')

SITE_READ_ONLY = True

MIDDLEWARE.append('readonly.middleware.DatabaseReadOnlyMiddleware')

DB_READ_ONLY_MIDDLEWARE_MESSAGE = True
