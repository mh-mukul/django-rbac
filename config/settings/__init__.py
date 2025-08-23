from .base import *

# Import environment specific settings
# Default to development settings
import os
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'dev')

if ENVIRONMENT == 'prod':
    from .prod import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    from .dev import *
