""" Run all tests that are for maya. This should be run via mayapy.exe

This script will exit with 0 if tests were successful and with 1 if tests failed.

First we find the maya installation. For this we use our platforminterfaces from :ref:`jukebox.core.ostool`.
Maya standalone needs some configuration. You can find it in the documentation
`Running Maya Standalone <http://download.autodesk.com/global/docs/maya2014/en_us/index.html?url=files/Python_Python_from_an_external_interpreter.htm,topicNumber=d30e815354>`_.

"""

if __name__ == '__main__':
    #for nicer log
    print "\n\nSTART OF MAYATEST"
    print "="*80

    import sys

    import jukebox.core.main
    jukebox.core.main.init_test_env()

    from jukebox.maya3d import start_maya_standalone
    from jukebox.tests import MAYA_TEST_ARGS

    # setup and run maya standalone
    start_maya_standalone(name='nosetest')

    # run the actual nose test now!
    import nose
    rcode = nose.run(argv=MAYA_TEST_ARGS)
    print ""
    print "="*80
    sys.stdout.write("RESULT OF MAYATESTS ... ")
    sys.exit(not int(rcode))  # False means test failed so convert it to 1
