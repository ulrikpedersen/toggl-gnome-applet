#!/usr/bin/env python

import logging
from datetime import datetime
logging.basicConfig(level=logging.WARNING)

import os
import urllib2, base64, json
import dateutil.parser

def from_ISO8601( str_iso8601 ):
    return dateutil.parser.parse(str_iso8601)

def to_ISO8601( timestamp ):
    return timestamp.isoformat()

def convert_time_strings(toggl_dicts):
    timestamp_fields = ['at',
                        'created_at',
                        'start',
                        'stop']
    result = []
    for tdict in toggl_dicts:
        d = tdict
        for tsf in timestamp_fields:
            if tdict.has_key(tsf):
                d[tsf] = from_ISO8601(tdict[tsf])
        result.append(d)
    return result

class Toggl:
    def __init__(self, api_token=None):
        self.log = logging.getLogger("Toggl")
        self.log.setLevel(logging.DEBUG)
        
        self.toggl_domain = "www.toggl.com"
        self.toggl_api = "https://%s/api/v8/" % self.toggl_domain
        self.report_api = "https://%s/reports/api/v2" % self.toggl_domain
        self._api_token = api_token

        # Search for an Toggl API token in a list of files
        # No validation of the collected token
        # TODO: encryption of tokenfiles could be nice
        tokenfiles = [os.path.expanduser(f) for f in ['.toggltoken', '~/.toggltoken']]
        for tf in tokenfiles:
            if os.path.exists( tf ):
                try:
                    f = open(tf)
                    self._api_token = f.read().strip()
                    f.close()
                except:
                    self.log.exception("Could not read token from " + tf)
                    self._api_token = None
            if self._api_token: break
        
                
    def send_request( self, api_call_url ):
        ''' Send a request or command to Toggl, retrieve and parse the json response.
        returns a list of dictionary objects.
        Throws an exception if the http response is not OK (200) or if no JSON can be decoded from the response.
        '''
        request = urllib2.Request( api_call_url )
        # username:password
        # Use base64.standard_b64encode instead of replace...
        user_pass = base64.encodestring('%s:%s' % (self._api_token, 'api_token')).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % user_pass)   
        result = urllib2.urlopen(request, timeout = 2.0) # with no data, this is a http GET.
        self.log.debug("http request result: code=%s url=\'%s\'", result.getcode(), result.geturl())
        js = json.load(result)
        #self.log.debug("JSON raw result: %s" % json.dumps(js,sort_keys=True, indent=4, separators=(',', ': ')))
        return js
    
    def get_workspaces(self):
        self.log.debug("get_workspaces()")
        js = self.send_request(self.toggl_api + "workspaces")
        js = convert_time_strings(js)
        return js
    
    def get_default_workspace(self):
        self.log.debug("get_default_workspace()")
        wid = self.get_user()['default_wid']
        js = self.send_request(self.toggl_api + "workspaces/%s"%str(wid))
        js = convert_time_strings([js['data']])
        return js[0]
    
    def get_default_workspace_id(self):
        self.log.debug("get_default_workspace_id()")
        ws = self.get_default_workspace()
        self.log.debug(ws)
        return ws['id']
    
    def get_projects(self, wid=None):
        self.log.debug("get_projects(wid=%s)"%str(wid))
        if wid:
            js = self.send_request(self.toggl_api + "workspaces/%s/projects"%str(wid))
        else:
            js = []
            for w in self.get_workspaces():
                js += self.send_request(self.toggl_api + "workspaces/%s/projects"%str(w['id']))
        js = convert_time_strings(js)
        return js
    
    def get_current_entry(self):
        '''get the currently active time entry'''
        self.log.debug("get_current_entry()")
        js = self.send_request(self.toggl_api + "time_entries/current")
        self.log.debug( js )
        js = convert_time_strings(js['data'])
        return js
        
    def get_range_entries(self, start_end=None):
        '''Get a list of entries in a range (max 1000 entries).
        If no start-end range is defined, the default is to return all entries
        from the last 9 days.
        start_end: tuple with start and end date'''
        self.log.debug("get_range_entries()")
        query = "time_entries"
        if start_end:
            start, end = start_end
            if type(start) == datetime.datetime:
                start = to_ISO8601(start)
            if type(end) == datetime.datetime:
                end = to_ISO8601(end)
            query += "?start_date=%s&end_date=%s"%(start, end)
        js = self.send_request(self.toggl_api + query)
        js = convert_time_strings(js)
        return js
            
    def get_user(self):
        self.log.debug("get_user()")
        js = self.send_request(self.toggl_api + "me")
        return js['data']

        