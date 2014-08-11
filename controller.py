'''
Created on 11 Aug 2014

@author: up45
'''

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
        
    
    