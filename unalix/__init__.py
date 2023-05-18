from unalix._core import clear_url, unshort_url
from unalix.__version__ import __description__, __title__, __version__
from unalix._exceptions import (
    InvalidURL,
    InvalidScheme,
    TooManyRedirects,
    ConnectError,
)

__all__ = [
    "__description__",
    "__title__",
    "__version__",
    "clear_url",
    "unshort_url",
    "InvalidURL",
    "InvalidScheme",
    "TooManyRedirects",
    "ConnectError",
]

__locals = locals()

for __name in __all__:
    if not __name.startswith("__"):
        setattr(__locals[__name], "__module__", "")
