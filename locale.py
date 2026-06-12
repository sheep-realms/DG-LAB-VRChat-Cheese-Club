import sys
from pathlib import Path

import i18n

_DEFAULT_LOCALE = 'zho-Hans'

def _get_locales_dir():
    p = Path(sys.executable if getattr(sys, "frozen", False) else sys.argv[0]).resolve().parent
    p = p / 'locales'
    return p.as_posix()

i18n.set('filename_format', '{locale}.{format}')
i18n.set('fallback', _DEFAULT_LOCALE)
i18n.load_path.append(_get_locales_dir())

def initTranslator(locale):
    i18n.set('locale', locale)
    i18n.load_everything()

def tr(key, **args):
    return i18n.t(key, **args)