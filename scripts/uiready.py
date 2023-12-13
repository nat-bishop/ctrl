"""
Startup Script to se tup hrpyc server for communication to houdini from external python scripts


Houdini will find any files matching this pattern in the Houdini path and run them after the UI is ready.
 You should use this script to set up interactive since when it runs the UI and UI scripting is available,
 and Houdini has loaded . Houdini only runs this script (if it exists) in interactive sessions. If your code
  needs assets to be loaded, but you want it available in both Houdini, batch mode, and hython, use ready.py instead.

For example, $HOUDINI_USER_PREF_DIR/pythonX.Ylibs/uiready.py for your personal script.
"""

import hrpyc
hrpyc.start_server(port=18812)