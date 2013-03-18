#!/usr/bin/env sh

echo "$( cd "$( dirname "${0}" )" && pwd )"

cd "$( cd "$( dirname "${0}" )" && pwd )"

echo Python versions: 

/usr/bin/env python2.7 --version
/usr/bin/env python3.2 --version

/usr/bin/env python2.7 test_all.py && /usr/bin/env python3.2 test_all.py



