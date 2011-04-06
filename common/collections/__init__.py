from UserDict import DictMixin

class OrderedDict(DictMixin):
    """Ordered key Dictionary
    
    >>> OrderedDict({'one': 2, 'two': 3})
    OrderedDict([('two', 3), ('one', 2)])
    >>> OrderedDict({'one': 2, 'two': 3}.items())
    OrderedDict([('two', 3), ('one', 2)])
    >>> OrderedDict({'one': 2, 'two': 3}.iteritems())
    OrderedDict([('two', 3), ('one', 2)])
    >>> OrderedDict(zip(('one', 'two'), (2, 3)))
    OrderedDict([('one', 2), ('two', 3)])
    >>> OrderedDict([['two', 3], ['one', 2]])
    OrderedDict([('two', 3), ('one', 2)])
    >>> OrderedDict(one=2, two=3)
    OrderedDict([('two', 3), ('one', 2)])
    >>> OrderedDict([(['one', 'two'][i-2], i) for i in (2, 3)])
    OrderedDict([('one', 2), ('two', 3)])
    >>> OrderedDict({'one': 1}, one=2)
    OrderedDict([('one', 2)])
    """
    
    def __init__(self, data=None, **kwdata):
        self._keys = []
        self._data = {}
        if data is not None:
            if hasattr(data, 'items'):
                items = data.items()
            else:
                items = list(data)
            for i in xrange(len(items)):
                length = len(items[i])
                if length != 2:
                    raise ValueError('dictionary update sequence element '
                        '#%d has length %d; 2 is required' % (i, length))
                self._keys.append(items[i][0])
                self._data[items[i][0]] = items[i][1]
        if kwdata:
            self._merge_keys(kwdata.iterkeys())
            self.update(kwdata)
    
    
    def __repr__(self):
        result = []
        for key in self._keys:
            result.append('(%s, %s)' % (repr(key), repr(self._data[key])))
        return ''.join(['OrderedDict', '([', ', '.join(result), '])'])
    
    def _merge_keys(self, keys):
        self._keys.extend(keys)
        newkeys = {}
        self._keys = [newkeys.setdefault(x, x) for x in self._keys
            if x not in newkeys]
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            result = [(k, self._data[k]) for k in self._keys[key]]
            return OrderedDict(result)
        return self._data[key]

    def __iter__(self):
        for key in self._keys:
            yield key

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)

    def keys(self):
        return list(self._keys)
    
    def copy(self):
        copyDict = OrderedDict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict
        
    def update(self, data):
        if data is not None:
            if hasattr(data, 'iterkeys'):
                self._merge_keys(data.iterkeys())
            else:
                self._merge_keys(data.keys())
            self._data.update(data)

if __name__ == "__main__":
    import doctest
    doctest.testmod()