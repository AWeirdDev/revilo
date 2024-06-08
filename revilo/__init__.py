import sys

assert (
    sys.platform != "darwin"
), "We're working on supporting Mac OS real soon. Hold, please!"
assert sys.platform == "win32", (
    "Unsupported platform: %s\nContribute to make it yours!" % sys.platform
)

from . import windows  # noqa: E402

__all__ = ["windows"]
