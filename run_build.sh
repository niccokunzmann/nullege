#!/usr/bin/env sh

echo "$( cd "$( dirname "${0}" )" && pwd )"

cd "$( cd "$( dirname "${0}" )" && pwd )"

echo 
echo Python version: 
/usr/bin/env python --version

ls /usr/bin

/usr/bin/env python2 test_all.py && /usr/bin/env python3 test_all.py



