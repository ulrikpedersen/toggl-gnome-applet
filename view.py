'''
Created on 12 Aug 2014

@author: up45
'''

import pygtk
pygtk.require('2.0')
import gtk

#import model

class View():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Basic TreeView Example")

        self.window.set_size_request(200, 200)

        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        self.liststore = None
        
        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.liststore)

        # create the TreeViewColumns to display the data
        self.id_col = gtk.TreeViewColumn('id')
        self.description_col = gtk.TreeViewColumn('description')
        self.project_col = gtk.TreeViewColumn('project')
        self.duration_col = gtk.TreeViewColumn('duration')

        # add columns to treeview
        self.treeview.append_column(self.id_col)
        self.treeview.append_column(self.description_col)
        self.treeview.append_column(self.project_col)
        self.treeview.append_column(self.duration_col)

        # create a CellRendererText to render the data
        self.id_cell = gtk.CellRendererText()
        self.description_cell = gtk.CellRendererText()
        self.project_cell = gtk.CellRendererText()
        self.duration_cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.id_col.pack_start(self.id_cell, True)
        self.description_col.pack_start(self.description_cell, True)
        self.project_col.pack_start(self.project_cell, True)
        self.duration_col.pack_start(self.duration_cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.id_col.add_attribute(self.id_cell, 'text', 0)
        self.description_col.add_attribute(self.description_cell, 'text', 1)
        self.project_col.add_attribute(self.project_cell, 'text', 2)
        self.duration_col.add_attribute(self.duration_cell, 'text', 3)

        # connect a click signal handler
        #self.treeview.connect("row-activated", self.on_click, 23)
        #self.liststore.connect("row-changed", self.row_changed, 24)

        self.window.add(self.treeview)

        self.window.show_all()
        
    def set_model(self, model):
        self.liststore = model
        self.treeview.set_model(self.liststore)
        
    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
        
