===========
Get Started
===========

----------------------
Developing the package
----------------------

If you are a pipeline developer, that wants to improve the jukebox pipeline directly
follow this guide:

  1. Clone the repository from either github or stash. See the in-depth description for git in the jukeboxcore documentation for more information.
  2. Read the python documentation of jukebox core on how to setup virtual environments and read the coding conventions.
     In short: make sure to have Python 2.7 installed. I recommend 64-bit version.
  3. Install jukemaya in development mode. Follow the :ref:`installation` guide but isntall jukebox maya like this::

       $ pip install -e path/to/jukeboxmayarepository

  4. If the psycopg2 dependency fails to install with pip, see :ref:`installation` for more information.
  5. Follow the database guide of jukebox core and make sure to have a configured database and userconfig.
  6. See :ref:`installation` on install the code for maya.
  7. Create a new gitbranch, write your code and tests. Read the :ref:`unittests` for more information on how to test.
     To simply test everything use::

       $ tox

  8. Commit your code. If tests are successful merge your branch in dev. See ref:`git` for more information
     on the branching model we use.


------------------------------
Developing a addon for jukebox
------------------------------

If you want to create addons for jukebox follow this guide:

  1. Make sure you have Python 2.7 installed. I recoomend the 64-bit version.
  2. Install jukeboxmaya as explained :ref:`here <installation>`.
  3. Follow the database guide of jukeboxcore and make sure to have a configured database and userconfig.
  4. Create folder or package for your addon code.
  5. Edit your ``pluginpaths`` in the userconfiguration and append the new folder to the paths.
     Multiple paths are seperated by either ``:`` on linux or ``;`` on windows.
     See the configuration guide of jukeboxcore for more information.
     Alternatively you can set the environment variable ``JUKEBOX_PLUGIN_PATHS``.
  6. Create a python file in your new folder and start coding the plugin.
     Create a new subclass from one of the :class:`jukeboxmaya.plugins.JB_MayaPlugin` classes and implement
     the abstract functions.
     The :class:`jukeboxmaya.plugin.MayaPluginManager` is used for loading and initializing the plugins.
