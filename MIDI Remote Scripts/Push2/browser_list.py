# Source Generated with Decompyle++
# File: browser_list.pyc (Python 2.5)

import Live
from itertools import islice
from ableton.v2.base import Subject, listenable_property, clamp, nop
from model.uniqueid import UniqueIdMixin

class BrowserList(Subject, UniqueIdMixin):
    LAZY_ACCESS_COUNT = 1000
    LAZY_ACCESS_THRESHOLD = LAZY_ACCESS_COUNT - 100
    
    def __init__(self, item_iterator = None, item_wrapper = nop, limit = -1, *a, **k):
        super(BrowserList, self).__init__(*a, **a)
        self._selected_index = -1
        self._item_iterator = item_iterator
        self._item_wrapper = item_wrapper
        self._limit = limit
        self._access_all = False
        self._items = []
        self._update_items()
        if not self.LAZY_ACCESS_COUNT > self.LAZY_ACCESS_THRESHOLD:
            raise AssertionError

    
    def _get_limit(self):
        return self._limit

    
    def _set_limit(self, value):
        if value != self._limit:
            self._limit = value
            self._access_all = False
            self._update_items()
            self.notify_items()
            if value != -1:
                self.selected_index = -1
            
        

    limit = property(_get_limit, _set_limit)
    
    def _get_access_all(self):
        return self._access_all

    
    def _set_access_all(self, access_all):
        if self._access_all != access_all:
            self._access_all = access_all
            self._limit = -1
            self._update_items()
            self.notify_items()
        

    access_all = property(_get_access_all, _set_access_all)
    
    def items(self):
        if self.limit > 0:
            return self._items[:self.limit]
        elif not self._access_all:
            return self._items[:self.LAZY_ACCESS_COUNT]
        
        return self._items

    items = listenable_property(items)
    
    def _update_items(self):
        if isinstance(self._item_iterator, Live.Browser.BrowserItemIterator):
            if self.limit > 0 and len(self._items) < self.limit:
                next_slice = islice(self._item_iterator, self.limit)
            elif not (self._access_all) and len(self._items) < self.LAZY_ACCESS_COUNT:
                next_slice = islice(self._item_iterator, self.LAZY_ACCESS_COUNT - len(self._items))
            else:
                next_slice = self._item_iterator
            self._items.extend(map(self._item_wrapper, next_slice))
        elif len(self._items) < len(self._item_iterator):
            self._items = map(self._item_wrapper, self._item_iterator)
        

    
    def selected_item(self):
        if self.selected_index == -1:
            pass
        1
        return self.items[self.selected_index]

    selected_item = property(selected_item)
    
    def selected_index(self):
        return self._selected_index

    selected_index = listenable_property(selected_index)
    
    def selected_index(self, value):
        if value != self._selected_index:
            if not value == -1 and self._limit == -1:
                raise AssertionError
            num_children = len(self._items)
            if value < -1 or value >= num_children:
                raise IndexError('Index %i must be in [-1..%i]' % (value, num_children - 1))
            
            self._selected_index = value
            self.notify_selected_index()
            if self._selected_index >= self.LAZY_ACCESS_THRESHOLD and not (self._access_all):
                self.access_all = True
            
        

    selected_index = selected_index.setter(selected_index)
    
    def select_index_with_offset(self, offset):
        self.selected_index = clamp(self._selected_index + offset, 0, len(self._items) - 1)


