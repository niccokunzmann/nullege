

try:
    from urllib.request import urlopen
except:
    from urllib import urlopen

class SourceNotFound(EOFError):
    """The source of the sample was not found"""

class Sample(object):
    def __init__(self, name, dict, index_in_request = None):
        self._name = name
        self._dict = dict
        self._index = index_in_request

    def _get(self, name):
        """get the value behind name"""
        return self._dict[name]

    @property
    def raw(self):
        """the dicionairy returned by the request"""
        return self._dict

    @property
    def index(self):
        """the index in the request
        None if this sample is not part of a request"""
        return self._index

    @property
    def name(self):
        """the name that was searched for"""
        return self._name

    @property
    def file(self):
        """the file path within the project"""
        return self._get('file')

    @property
    def line_numbers(self):
        """the lines where the object occurs as integers"""
        return list(map(int, self.raw_lines))

    @property
    def raw_lines(self):
        """the lines in raw format as returned by json"""
        return self._get('lines')

    @property
    def nullege_file_url(self):
        """the url of the source of the file on the nullege website"""
        return self._get('nullege_file')

    @property
    def project(self):
        """the name of the project the file is from"""
        return self._get('project')

    @property
    def repository(self):
        """the ropository of the project
        it can be a valid http or https url, a git file or svn root or
        an archive or even more"""
        return self._get('repository')

    @property
    def source(self):
        """the source of the file where the samples occur.
    if possible, it will be decoded"""
        return self._get_url(self.nullege_file_url)

    @property
    def source_lines(self):
        """the source as lines"""
        return self.source.splitlines()

    _urlopen = staticmethod(urlopen)
    
    def _get_url(self, url):
        """return the content behind the url"""
        request = self._urlopen(url)
        if request.status != 200:
            raise SourceNotFound('request to {url} had an error code {code}' \
                                 ''.format(url = url, code = request.status))
        source = request.read()
        charset = request.info().get_charset()
        if charset:
            source = source.decode(charset)
        elif hasattr(source, 'decode'):
            source = source.decode('utf8')
        return source

    def _lines_around(self, line_number, number_of_lines_in_sample):
        """return a number_of_lines around the line, start and end"""
        plus = (number_of_lines_in_sample) // 2
        minus = number_of_lines_in_sample - plus
        end = line_number + plus
        start = line_number - minus
        return self.source_lines[start: end], start, end

    def lines_around(self, line_number, number_of_lines = 5):
        """return a number_of_lines around the line"""
        return self._lines_around(line_number, number_of_lines)[0]

    def sample_lines(self, number_of_lines_in_sample = 5):
        """a list of lines from the source where the name occurs"""
        source_lines = self.source_lines
        sample_lines = [self._lines_around(line_number, number_of_lines_in_sample)\
                        for line_number in self.line_numbers]
        result = [sample_lines[0][0]]
        for s1, s2 in zip(sample_lines, sample_lines[1:]):
            if s1[2] >= s2[1]:
                result[-1] += s2[0][s1[2] - s2[1]:]
            else:
                result.append(s2[0])
        return result
        
            


