import imp
from nose.tools import *
from schemepy.scheme import *
import schemepy
import schemepy.evaluator as ev
import schemepy.reader as rd


def setup_func():
    ev = imp.reload(schemepy)

@with_setup(setup_func)
def test_single_expression_evaluation():
    expression = [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2) ]
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

@with_setup(setup_func)
def test_nested_expression_evaluation():
    expression = [SchemeSymbol('+'), SchemeNumber(1), [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2) ]]
    assert_equal(ev.evaluate(expression), SchemeNumber(4))

@with_setup(setup_func)
def test_primitive_evaluation():
    expression = SchemeNumber(1)
    assert_equal(ev.evaluate(expression), SchemeNumber(1))

@with_setup(setup_func)
def test_multi_line_evaluation():
    expression = rd.parse("(begin (+ 1 1) (+ 2 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(4))

@with_setup(setup_func)
def test_variable_defines():
    expression = rd.parse("(begin (define x 5) x)")
    assert_equal(ev.evaluate(expression).value, 5)

@with_setup(setup_func)
def test_define_exception():
    expression = rd.parse("(define x)")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_lamba():
    expression = rd.parse("(begin (define z (lambda (x y) (+ x y))) (z 1 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

@with_setup(setup_func)
def test_lambda_exception():
    expression = rd.parse("(lambda (x y z) )")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_lambda_no_params():
    expression = rd.parse("(begin (define func (lambda () (+ 1 1))) (func)) ")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))

@with_setup(setup_func)
def test_higherorder_functions():
    expression = rd.parse("(begin (define scons (lambda (x y) (lambda (m) (m x y)))) (define scar (lambda (z) (z (lambda (p q) p)))) (scar (scons 10 11)))")
    assert_equal(ev.evaluate(expression), SchemeNumber(10))

@with_setup(setup_func)
def test_lambda_shorthand():
    expression = rd.parse("(define (add a b) (+ a b)) (add 2 3)")
    assert_equal(ev.evaluate(expression), SchemeNumber(5))

@with_setup(setup_func)
def test_enviornments():
    expression = rd.parse("(begin (define b 3) (define fun (lambda (z) b)) (fun 1))")
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

@with_setup(setup_func)
def test_plus():
    expression = rd.parse("(+ 1 2 3)")
    assert_equal(ev.evaluate(expression), SchemeNumber(6))

@with_setup(setup_func)
def test_minus():
    expression = rd.parse("(- 5 2 3)")
    assert_equal(ev.evaluate(expression), SchemeNumber(0))

@with_setup(setup_func)
def test_times():
    expression = rd.parse("(* 5 2 3)")
    assert_equal(ev.evaluate(expression), SchemeNumber(30))

@with_setup(setup_func)
def test_divide():
    expression = rd.parse("(/ 100 10 5)")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))

@with_setup(setup_func)
def test_equals():
    expression = rd.parse("(= 3 3)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(= 3 1)")
    assert_equal(ev.evaluate(expression), SchemeFalse())
    expression = rd.parse("(= 3 3 3)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(= 3 1 1)")
    assert_equals(ev.evaluate(expression), SchemeFalse())

@with_setup(setup_func)
def test_greater():
    expression = rd.parse("(> 10 1)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(> 10 5 4 3 2 1)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(> 10 5 4 4 2 1)")
    assert_equal(ev.evaluate(expression), SchemeFalse())
    expression = rd.parse("(> 10 5 4 5 2 1)")
    assert_equal(ev.evaluate(expression), SchemeFalse())

@with_setup(setup_func)
def test_greater_equals():
    expression = rd.parse("(>= 10 1)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(>= 10 5 4 3 2 1)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(>= 10 5 4 4 2 1)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(>= 10 5 4 5 2 1)")
    assert_equal(ev.evaluate(expression), SchemeFalse())
    expression = rd.parse("(>= 10 10 10 10 10 10)")
    assert_equal(ev.evaluate(expression), SchemeTrue())

@with_setup(setup_func)
def test_less():
    expression = rd.parse("(< 1 10)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(< 1 2 3 4 5 10)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(< 1 2 3 4 4 5 10)")
    assert_equal(ev.evaluate(expression), SchemeFalse())
    expression = rd.parse("(< 1 2 3 4 3 1)")
    assert_equal(ev.evaluate(expression), SchemeFalse())

@with_setup(setup_func)
def test_less_equals():
    expression = rd.parse("(<= 1 10)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(<= 1 2 3 5 6 10)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(<= 1 2 3 4 4 5 10)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(<= 1 2 3 4 3 10)")
    assert_equal(ev.evaluate(expression), SchemeFalse())
    expression = rd.parse("(<= 10 10 10 10 10 10)")
    assert_equal(ev.evaluate(expression), SchemeTrue())

@with_setup(setup_func)
def test_and():
    expression = rd.parse("(and #t #t)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(and #t #t #t)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(and #t #t #f)")
    assert_equal(ev.evaluate(expression), SchemeFalse())

@with_setup(setup_func)
def test_or():
    expression = rd.parse("(or #t #f)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(or #t #t #t)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(or #f #f #f)")
    assert_equal(ev.evaluate(expression), SchemeFalse())

@with_setup(setup_func)
def test_not():
    expression = rd.parse("(not #f)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(not #t)")
    assert_equal(ev.evaluate(expression), SchemeFalse())

@with_setup(setup_func)
def test_if():
    expression = rd.parse("(if (= 3 3) 1 2)")
    assert_equal(ev.evaluate(expression), SchemeNumber(1))
    expression = rd.parse("(if (= 3 1) 1 2)")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))

@with_setup(setup_func)
def test_if_exception():
    expression = rd.parse("(if (= 1 1) 1)")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_cons():
    expression = rd.parse("(cons 1 2)")
    exp = ev.evaluate(expression)
    assert_true(ev.evaluate(expression) == SchemeCons(SchemeNumber(1),SchemeNumber(2)))
    expression= rd.parse("(cons (+ 1 2) (+ 3 4 ))")
    assert_equal(ev.evaluate(expression), SchemeCons(SchemeNumber(3), SchemeNumber(7)))

@with_setup(setup_func)
def test_cons_exception():
    expression = rd.parse("(cons 1)")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_car():
    expression = rd.parse("(car (cons 1 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(1))

@with_setup(setup_func)
def test_car_exception():
    expression = rd.parse('(car (cons 1 2) (cons 1 2))')
    assert_raises(SchemeException, ev.evaluate, expression)

    expression = rd.parse('(car 1)')
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_cdr():
    expression = rd.parse("(cdr (cons 1 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))

@with_setup(setup_func)
def test_cdr_exception():
    expression = rd.parse('(cdr (cons 1 2) (cons 1 2))')
    assert_raises(SchemeException, ev.evaluate, expression)

    expression = rd.parse('(cdr 1)')
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_let():
    expression = rd.parse("(let ((a 1) (b 1)) (+ a b))")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))

@with_setup(setup_func)
def test_let_exception():
    expression = rd.parse("(let (a))")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_shorthand_lambda():
    define_short = rd.parse("(define (test (a b) (+ a b)))")

@with_setup(setup_func)
def test_syntax_error():
    expression = rd.parse("(quote 12 23)")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_set_test():
    define_singleton_set = rd.parse("(define singletonSet (lambda (x) (lambda (y) (= y x))))")
    define_contains = rd.parse("(define contains (lambda (set_ y) (set_ y)))")
    define_test_sets = rd.parse("""(begin
        (define s1 (singletonSet 1))
        (define s2 (singletonSet 2))
        (define s3 (lambda (x) (and (>= x 5) (<= x 15))))
        (define s4 (lambda (x) (and (<= x -5) (>= x -15))))
         )""")

    test_1 = rd.parse("(contains s1 1)")
    test_2 = rd.parse("(contains s2 2)")
    test_3 = rd.parse("(contains s3 5)")
    test_4 = rd.parse("(contains s4 -5)")
    test_5 = rd.parse("(contains s4 -22)")

    ev.evaluate(define_singleton_set)
    ev.evaluate(define_contains)
    ev.evaluate(define_test_sets)

    assert_equal(ev.evaluate(test_1), SchemeTrue())
    assert_equal(ev.evaluate(test_2), SchemeTrue())
    assert_equal(ev.evaluate(test_3), SchemeTrue())
    assert_equal(ev.evaluate(test_4), SchemeTrue())
    assert_equal(ev.evaluate(test_5), SchemeFalse())


@with_setup(setup_func)
def test_list_eval():
    define_list = rd.parse("""
    (begin (define foo (lambda () 4))
            (define bar (lambda () foo))

            ((bar)))
    """)
    assert_equal(ev.evaluate(define_list), SchemeNumber(4))

@with_setup(setup_func)
def test_list_no_exec():
    define_list = rd.parse("""
    (begin
            (define baz (lambda () (cons 1 2)))
            ((baz))
    )
    """)
    assert_raises(SchemeException, ev.evaluate, define_list)

@with_setup(setup_func)
def test_Y_combinator():
    define_y = rd.parse("""
            (begin
            (define Y
             (lambda (f)
             ((lambda (x) (x x))
             (lambda (g)
             (f (lambda (x) ((g g) x)))))))
               (define fac
                 (Y
                   (lambda (f)
                     (lambda (x)
                       (if (< x 2)
                           1
                           (* x (f (- x 1)))))))))
""")
    define_test = rd.parse("(fac 6)")
    ev.evaluate(define_y)

    assert_equal(ev.evaluate(define_test), SchemeNumber(720))


@with_setup(setup_func)
def test_iota():
    define_iota = rd.parse("""(define iota (lambda (start end step) (begin (define helper (lambda (cur list) (if (= cur start) list (helper (- cur step) (cons cur list))))) (helper end '()))))""")
    define_test = rd.parse("(iota 10 1 -1)")

    ev.evaluate(define_iota)

    assert_equal(str(ev.evaluate(define_test)), "(9 8 7 6 5 4 3 2 1)")