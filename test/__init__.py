# make this a package and import all tests

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from nullege.test.test import *
from nullege.test.test_Sample import *
from nullege.test.test_find import *
