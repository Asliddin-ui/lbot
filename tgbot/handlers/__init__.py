from .start import handlers as start_handlers
from .registration import handlers as registration
from .settings import handlers as settings
handlers = start_handlers + registration + settings
