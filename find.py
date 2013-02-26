import json
try:
    # python3
    from urllib.request import urlopen
    from urllib.parse import quote
except ImportError:
    # python2
    from urllib import quote
    from urllib import urlopen


def nullege_json(string, start = 0, count = 10):
    string = quote(string)
    start = int(start)
    count = int(count)
    url = 'http://nullege.com/api/codes/search'\
          '?cq={string}&count={count}&start={start}'.format(**locals())
    request = urlopen(url)
    charset = request.info().get_charset()
    if not charset:
        charset = 'utf8'
    string = request.read().encode(charset)
    return json.loads(string)

def find_str(string):
    pass # TODO
    
