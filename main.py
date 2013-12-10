import schemepy.reader as rd
import schemepy.evaluator as ev

ast = rd.parse("(begin (define x 1) x)")
ev.evaluate(ast)