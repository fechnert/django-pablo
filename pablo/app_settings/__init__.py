from .defaults import *
from django import conf


# merge defaults with customized user settings

for setting_name in [k for k in globals().keys() if k.isupper()]:
        for name in ["PABLO_" + setting_name, setting_name]:
            try:
                globals()[setting_name] = getattr(conf.settings, name)
                continue
            except (KeyError, AttributeError):
                pass  # not set
