'''
Created on 11 Aug 2014

@author: up45
'''

import toggl
import threading
from datetime import datetime

class IViewModel:
    def get_projects(self):
        '''Return a list of project titles'''
        raise NotImplementedError
    def get_time_entries(self):
        '''Return a list of time entry dictionaries.
        Default: {'project': "", 'description': "", 'duration': None}'''
        raise NotImplementedError
    def register_for_notification(self, func):
        '''Register a callable or function for a callback nofication when the 
        model detects a change in state.'''
        raise NotImplementedError
    
class IControlModel:
    def update(self):
        '''Non-blocking command to update the model data'''
        raise NotImplementedError

class TogglModel(IControlModel, IViewModel):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.toggl = toggl.Toggl()
        self.projects = []
        self.time_entries = []
        
        self.notifiers = []
        self._lock = threading.Lock()
    
    # Controller interface
    def update(self):
        thread = threading.Thread(target=self._get_updates)
        thread.start()
    
    
    # View interface
    def register_for_notification(self, func):
        self.notifiers.append( func )
        
    def get_projects(self):
        self._lock.acquire()
        try:
            projects = [p['name'] for p in self.projects]
        finally:
            self._lock.release()
        return projects

    def get_time_entries(self):
        self._lock.acquire()
        entries = []
        try:
            for entry in self.time_entries:
                d = {'project': "", 'description': "", 'duration': None}
                if entry.has_key('pid'):
                    # lookup the project name in project list
                    try:
                        i = next(index for (index,d) in enumerate(self.projects) if d['id'] == entry['pid'])
                        d['project'] = self.projects[i]
                    except:
                        pass
                if entry.has_key('description'):
                    d['description'] = entry['description']
                if entry.has_key('start'):
                    if entry.has_key('end'):
                        d['duration'] = entry['end'] - entry['start']
                    #else:
                    #    d['duration'] = datetime.now() - entry['start']
                entries.append(d)
        finally:
            self._lock.release()
        return entries    
    
    
    # Implementation
    def _get_updates(self):
        '''Query toggl for updates and notify any listeners'''
        dirty=False
        projects = self._get_toggl_projects()
        ts_entries = self._get_toggl_time_entries()

        self._lock.acquire()
        if not self.projects == projects:
            dirty=True
        self.projects = projects
        
        if not self.time_entries == ts_entries:
            dirty = True
        self.time_entries = ts_entries
        self._lock.release()
        
        if dirty:
            self._notify_projects_change()    
    
    def _get_toggl_projects(self):
        '''Return a sorted list of projects'''
        wid = self.toggl.get_default_workspace_id()
        # Sorted by project ID number
        projects = self.get_projects(wid) 
        self._convert_time_strings(projects)
        return sorted(projects, key=lambda k: k['id'])
    
    def _get_toggl_time_entries(self):
        entries = self.toggl.get_range_entries()
        self._convert_time_strings(entries)
        return entries
        
    def _convert_time_strings(self, toggl_dicts):
        timestamp_fields = ['at',
                            'created_at',
                            'start',
                            'stop']
        for tdict in toggl_dicts:
            for tsf in timestamp_fields:
                try:
                    tdict[tsf] = toggl.from_ISO8601(tdict[tsf])
                except:
                    pass
    
    def _notify_projects_change(self):
        for notify_cb in self.notifiers:
            notify_cb()
        
    