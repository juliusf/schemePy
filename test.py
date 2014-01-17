

import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
from schemepy.stream import Stream


stream = Stream('(define (add a b) (+ a b)) (add 2 3)')
foo = rd._parse_helper(stream)
print(foo)
