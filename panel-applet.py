#!/bin/env python2.6
'''
Created on Aug 12, 2014

@author: up45
'''
if __name__ == '__main__':
    try:
        from pkg_resources import require
        require('python-dateutil')
    except:
        pass
    
import sys
import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet

import view, model

class PanelApplet:
    def __init__(self):
        self.appwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.appwin.set_decorated(False)
        self.appwin.set_default_size(400,300)
        self.appwin.set_position(gtk.WIN_POS_MOUSE) # This is the magic that makes the window appear by the applet button
        self.appwin.set_has_frame(False)
        self.appwin.set_border_width(0)
        self.appwin.set_skip_taskbar_hint(True)

        
    def button_press(self, button, event):
        print button, event
        if event.button == 1:
            if self.appwin.get_property('visible'):
                self.appwin.hide()
            else:
                self.appwin.show_all()
        else:
            return False
        
    def factory(self, applet, iid):
        print applet
        print iid
        # homebrew MVC
        V = view.View()
        M = model.TogglModel()
        V.set_model(M.generate_liststore())
        self.appwin.add(V.treeview)
        self.appwin.resize(400,300)
        #self.appwin.add(gtk.Label('hi there'))
        
        im = gtk.Image()
        im.set_from_file("/home/up45/github/toggl-gnome-applet/logo-small.png")
        ebox = gtk.EventBox()
        
        ebox.add(im)
        ebox.connect('button-press-event', self.button_press)
        #applet.set_background_widget(applet)
        #applet.connect('button-press-event',button_press)
        applet.add(ebox)
        
       
        applet.show_all()
        print applet.window

        return gtk.TRUE

    
if __name__ == '__main__':
    papplet = PanelApplet()
    
    if len(sys.argv) == 2:
        if sys.argv[1] == "run-in-window":
            mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
            mainWindow.set_title("Toggl applet")
            mainWindow.connect("destroy", gtk.main_quit)
            # gnome bonobo applet stuff
            applet = gnomeapplet.Applet()
            papplet.factory(applet, None)
            applet.reparent(mainWindow)
            mainWindow.show_all()
            gtk.main()
            sys.exit()
    else:
        #print "Starting gnomeapplet bonobo"
        gnomeapplet.bonobo_factory("OAFIID:GNOME_TogglApplet_Factory", 
                                     gnomeapplet.Applet.__gtype__, 
                                     "toggl", "0", papplet.factory)
        
