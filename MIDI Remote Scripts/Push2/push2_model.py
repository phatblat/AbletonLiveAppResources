# Source Generated with Decompyle++
# File: push2_model.pyc (Python 2.5)

import os
import sys
from pprint import pformat
import logging
j = os.path.join
dn = os.path.dirname
sys.path.append(j(dn(dn(__file__)), '_Tools'))
import simplejson as json
from model import RootModel
from model.generation import generate_mrs_model, ModelUpdateNotifier
logger = logging.getLogger(__name__)

class Sender(object):
    
    def __init__(self, message_sink = None, process_connected = None, *a, **k):
        super(Sender, self).__init__(*a, **a)
        if not message_sink is not None:
            raise AssertionError
        self._message_sink = message_sink
        if process_connected is None:
            
            process_connected = lambda : True
        
        self._process_connected = process_connected
        self._attribute_paths = []
        self._structural_change = False
        self.notifier = ModelUpdateNotifier(delegate = self)

    
    def structural_change(self, path):
        self._attribute_paths.append((path, None))
        self._structural_change = True

    
    def attribute_changed(self, path, value):
        self._attribute_paths.append((path, value))

    
    def send(self, root_model, send_all = False):
        
        def send_data(data):
            raw = json.dumps(data)
            self._message_sink(raw)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Model sent: %s', pformat(data))
            

        if send_all:
            send_data(dict(command = 'full-model-update', payload = root_model.to_json()))
        elif self._structural_change:
            root_keys = set(lambda .0: for path in .0:
path[0][0](self._attribute_paths))
            data = dict(command = 'full-model-update', payload = root_model.to_json(root_keys))
            send_data(data)
        elif self._attribute_paths:
            data = dict(command = 'path-model-update', payload = self._attribute_paths)
            send_data(data)
        
        self._attribute_paths = []
        self._structural_change = False



class Root(generate_mrs_model(RootModel)):
    
    def __init__(self, sender = None, *a, **k):
        self._sender = sender
        if sender is not None:
            k['notifier'] = sender.notifier
        
        super(Root, self).__init__(*a, **a)

    
    def commit_changes(self, send_all = False):
        if self._sender is not None:
            self._sender.send(self, send_all)
        

    
    def to_json(self, root_keys = None):
        if root_keys is None:
            return super(Root, self).to_json()
        else:
            res = { }
            for key in root_keys:
                res[key] = self.data[key].to_json()
            
            return res


