toggl-gnome-applet
==================

a simple toggl time tracking gnome panel applet


Requirements
------------
 
 * pygtk2
 * python-dateutil (if using python 2.6)


 Configuring Bonobo
 ------------------
 
 In order for bonobo to find the applet, it searches for the .server files. The search path can be configured by setting an environment variable in your .bash_profile:
 
export BONOBO_ACTIVATION_PATH=$HOME/.bonobo
 
Also create the $HOME/.bonobo folder and in there softlink to the .server files

