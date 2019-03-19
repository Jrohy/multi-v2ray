__version__ = '3.0.6'

import gettext
import pkg_resources

gettext.translation('lang', pkg_resources.resource_filename('v2ray_util', 'locale_i18n'), languages=['zh_CH']).install()