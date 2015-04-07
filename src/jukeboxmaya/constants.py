""" Define constant values that matter for the whole pipeline here """

import os

_norm = os.path.normpath  # make it shorter

here = os.path.abspath(os.path.dirname(__file__))

BUILTIN_PLUGIN_PATH = _norm(os.path.join(here, 'addons'))

MAYA_PLUGIN_PATH = _norm(os.path.join(here, 'mayaplugins'))
"""A path to maya plugins. These plugins are managed by mayas intern plugin management system. Do not confuse them with jukebox plugins."""
