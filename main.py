import schemepy.reader as rd
import schemepy.evaluator as ev

ast = rd.parse("(begin (define z (lambda (x y) (+ x y))) (z 1 2))")
ev.evaluate(ast)
