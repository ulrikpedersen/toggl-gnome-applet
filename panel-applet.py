#!/bin/env python2.6
'''
Created on Aug 12, 2014

@author: up45
'''

import sys
import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet

import view, model
def button_press(button, event):
    print button, event
    
def factory(applet, iid):
    # homebrew MVC
    V = view.View()
    M = model.TogglModel()
    V.set_model(M.generate_liststore())

    #applet.add(V.treeview)
    
    im = gtk.Image()
    im.set_from_file("/home/up45/develop/toggl-gnome-applet/logo-small.png")
    applet.set_background_widget(applet)
    applet.connect('button-press-event',button_press)
    applet.add(im)
    
    applet.show_all()
    return gtk.TRUE

    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "run-in-window":
            mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
            mainWindow.set_title("Toggl applet")
            mainWindow.connect("destroy", gtk.main_quit)
            # gnome bonobo applet stuff
            applet = gnomeapplet.Applet()
            factory(applet, None)
            applet.reparent(mainWindow)
            mainWindow.show_all()
            gtk.main()
            sys.exit()
    else:
        #print "Starting gnomeapplet bonobo"
        gnomeapplet.bonobo_factory("OAFIID:GNOME_TogglApplet_Factory", 
                                     gnomeapplet.Applet.__gtype__, 
                                     "toggl", "0", factory)
        # Create the gnome panel icon

        #icon = gtk.StatusIcon()
        #icon.set_from_file("toggl-icon.png")
        #icon.set_tooltip("Toggl Timer")
        # homebrew MVC
        #V = view.View()
        #M = model.TogglModel()
        #V.set_model(M.generate_liststore())

        #icon.connect('popup-menu', popup_menu, V.treeview)
        #gtk.main()
        