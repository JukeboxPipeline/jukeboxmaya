.. _installation:

============
Installation
============

There are several ways to install jukebox-maya.
One way would be to install it directly into the sitepackage dir of maya. The only problem is, that you need to configure
your environment to use the maya python intepreter and have admin rights.

To work around that you could also install jukebox-maya into a virutal environment and modify your ``Maya.env`` and ``userSetup.py``
slightly:

  1. Install Python 2.7 64-bit.
  2. Install virtual env::

       $ pip install virtualenv

  3. Create a virtual env on some location where you do not need admin rights. Go to that location and use::

       $ virtualenv ENV

     This will install a new virtual env in the folder ``ENV``. So change the name accordingly.

  4. Activate the virtual environment. On posix::

       $ source bin/activate

     On windows::

       $ scripts/activate

  5. Install the psycopg2 dependency. See the jukebox-core documentation in the user manual section under **Installation** on how to do that.
  6. Install jukebox-maya::

       $ pip install jukebox-maya

  7. Add the virtual environment paths to your ``Maya.env``. Add this line on linux::

       PATH = path/to/env/Lib/site-packages:path/to/env/Include:path/to/env/Scripts:

     or on windows::

       PATH = path\to\env\Lib\site-packages;path\to\env\Include;path\to\env\Scripts;

  8. Add these lines to your ``userSetup.py``::

       import maya.utils
       import site
       site.addsitedir(r"path/to/env/Lib/site-packages")
       import jukeboxmaya.main
       maya.utils.executeDeferred(jukeboxmaya.main.init)

  9. Start Maya and check the new Jukebox menu entry.
