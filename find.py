""" Module for finding samples

use sample() instead of help() to get usage samples for the given object

    >>> samples(bytearray)
    protocyt

        def test_serialize():
            tree.serialize(bytearray())

        def test_deserialize(ba):


        ba = bytearray()
        tree.serialize(ba)
        data = pickle.dumps(tree, 2)

        def test_serialize():
            ba = bytearray()
            tree.serialize(ba)
            return len(ba)

find_samples returns a Samples listing.

    >>> find_samples(bytearray)
    <__main__.Samples object at 0x03BAB030>

#TODO: add Samples.fetch to make it faster

"""

import json
import sample

try:
    # python3
    from urllib.request import urlopen
    from urllib.parse import quote
except ImportError:
    # python2
    from urllib import quote
    from urllib import urlopen

MAXIMUM_NUMBER_OF_SAMPLES_TO_LOAD = 100

def nullege_url(string, start = 0, count = 10):
    """return the url at nullege.com where the json can be retrieved from"""
    assert 0 <= count <= MAXIMUM_NUMBER_OF_SAMPLES_TO_LOAD
    string = quote(string)
    start = int(start)
    count = int(count)
    return 'http://nullege.com/api/codes/search'\
          '?cq={string}&count={count}&start={start}'.format(**locals())

def nullege_json(url):
    """load the json for count samples from the nullege website
    staring at start
    use nullege_url to get the url"""
    request = urlopen(url)
    charset = request.info().get_charset()
    if not charset:
        charset = 'utf8'
    string = request.read().decode(charset)
    return json.loads(string)

class Samples(object):
    """a class for a collection of samples
    the class is iterable"""
    _nullege_json = staticmethod(nullege_json)
    _nullege_url = staticmethod(nullege_url)
    samples_to_load_at_once = MAXIMUM_NUMBER_OF_SAMPLES_TO_LOAD

    _new_sample = sample.Sample
    
    def __init__(self, string):
        """Create an iterable search result for the string"""
        self._searchString = string
        self._samples = {} # (start index, end index) -> [listofsamples]
        self._length = 0

    def __len__(self):
        """the count of loaded samples"""
        return sum(map(len, self._samples.values()))

    def _get_local_sample(self, index, default = None):
        """get the sample at index but do not load from the internet
        if the index is too high, default is returned"""
        for key in self._samples:
            if index < key[0] or index >= key[1]:
                continue
            position = index - key[0]
            if not 0 <= position < len(self._samples[key]):
                # no results any more
                return default
            return self._samples[key][position]
        return default

    def get(self, index, default = None):
        """get a sample at index, if index is too high, default is returned"""
        _default = []
        sample = self._get_local_sample(index, _default)
        if sample is _default:
            self._load_sample(index)
        return self._get_local_sample(index, default)

    def _load_sample(self, index):
        """load the sample at index if it was not not loaded before"""
        count = self.samples_to_load_at_once
        start = index - index % count
        end = start + count
        if (start, end) in self._samples:
            return 
        json = self._nullege_json(self._nullege_url(self.name, start, count))
        name = json['name']
        samples = []
        for sample_offset, sample_json in enumerate(json['samples']):
            samples.append(self._new_sample(name, sample_json, start + sample_offset))
        if len(samples) != count:
            self._length = start + len(samples)
        self._samples[(start, end)] = samples

    def __getitem__(self, index):
        """return the sample at index
        raises IndexError if sample could not be found"""
        default = []
        sample = self.get(index, default)
        if sample is default:
            raise IndexError('sample index %s out of range' % index)
        return sample

    @property
    def name(self):
        """the name that was searched for"""
        return self._searchString

    def __iter__(self):
        """iterate over the samples"""
        index = 0
        default = []
        while 1:
            sample = self.get(index, default)
            if sample is default:
                raise StopIteration(index)
            yield sample
            index += 1


def find_samples(obj):
    """the object can be a string or an object"""
    if isinstance(obj, str):
        string = obj
    else:
        if isinstance(obj.__class__, type) \
            or hasattr(obj, '__module__') and hasattr(obj, '__name__') or \
            hasattr(obj, '__qualname__'):
            cls = obj
        else:
            cls = obj.__class__
        string = get_qual_name(cls)
    return Samples(string)
    

def get_qual_name(obj):
    """return the qualified name of the object for the search with nullege"""
    if hasattr(obj, '__qualname__'):
        return obj.__qualname__
    if hasattr(obj, '__name__') and hasattr(obj, '__module__'):
        return obj.__module__ + '.' + obj.__name__
    raise AttributeError('no attributes found the make a usable string ' \
                         'out oj the object')

def change_line_identitation(lines, spaces = 4):
    """change the minimum identation of the given lines to the given amount of whitespaces"""
    min_ident = min([len(line) - len(line.lstrip()) for line in lines if \
                     line.lstrip() and line.lstrip()[0] != "#"])
    if min_ident > spaces:
        return [line[min_ident - spaces:] for line in lines]
    return [(spaces - min_ident) * ' ' + line for line in lines]
        
    
def sample(obj, count = 5):
    """print samples where the object is used"""
    for i, sample in enumerate(find_samples(obj)):
        if i >= count: break
        if i != 0:
            print()
        print(sample.project)
        for i, lines in enumerate(sample.sample_lines(5)):
            print('\n'.join(change_line_identitation(lines)))
        

__all__ = ['sample', 'Samples', 'find_samples', 'nullege_url', 'nullege_json']

if __name__ == '__main__':
    sample('bytearray')
    
