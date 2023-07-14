__version__ = '3.11.4'

import sys
if "xray" in sys.argv[0]:
    run_type = 'xray'
else:
    run_type = 'v2ray'

from .util_core.trans import _