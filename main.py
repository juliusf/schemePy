import schemepy.reader as rd
import schemepy.evaluator as ev

ast = rd.parse("(begin (define x 3) (define fun (lambda (z) x)) (fun 1))")
ret = ev.evaluate(ast)
print(ret)