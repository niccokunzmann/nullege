#!/usr/bin/env sh

echo "$( cd "$( dirname "${0}" )" && pwd )"

cd "$( cd "$( dirname "${0}" )" && pwd )"

/usr/bin/env python2 test_all.py
/usr/bin/env python3 test_all.py

