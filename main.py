import schemepy.reader as rd
import schemepy.evaluator as ev

ast = rd.parse("(+ 3 2)")
ev.evaluate(ast)