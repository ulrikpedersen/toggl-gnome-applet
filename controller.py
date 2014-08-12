'''
Created on 11 Aug 2014

@author: up45
'''
import pygtk
pygtk.require('2.0')
import gtk

import model, view

class Controller:
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.model = None
        self.view = None
        
    def set_model(self, model):
        self.model = model
        
    def set_view(self, view):
        self.view = view
        
    
    # View interface
    
    def list_projects(self):
        self.model.update()
    
    def list_entries(self):
        self.model.update()
        
    
def main():
    gtk.main()

if __name__ == "__main__":
    V = view.View()
    M = model.TogglModel()
    V.set_model(M.generate_liststore())
    main()
