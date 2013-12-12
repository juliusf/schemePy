import schemepy.reader as rd
import schemepy.evaluator as ev

ast = rd.parse("(begin (define scons (lambda (x y) (lambda (m) (m x y)))) (define scar (lambda (z) (z (lambda (p q) p)))) (scar (scons 10 11)))")
ev.evaluate(ast)
