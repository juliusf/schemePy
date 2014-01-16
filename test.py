

import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
from schemepy.stream import Stream


stream = Stream("(+ 2.0 (+ 1 2))")
foo = rd.parse_new(stream)
print(foo)
