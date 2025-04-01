from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, default_limits=["10000 per hour", "2000 per minute"], storage_uri="memory://")
