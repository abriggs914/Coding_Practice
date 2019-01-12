#lang racket
;; CS2613 midterm exam q1
;; Oct. 25 2018
;; Avery Briggs
;; 3471065

;; I couldn't seem to get this one working right. I believe that it is an issue
;; with my recursive calls to tree-map. Because of the error, the function returns
;; the base case, every time, once it has cycle through the list.
#|
(define (tree-map func lst)
  (define (helper func lst)
    (cond
      [(empty? lst) lst] ;; base case
      [else (cons (func (first lst)) (rest lst)) (helper func (rest lst))]))
  (helper func lst))
|#

(define (helper func acc lst)
  (cond
    [(empty? lst) acc]
    [(list? (first lst)) (helper func (cons (tree-map func (first lst)) acc)(rest lst))]
    [else (helper func (cons (func (first lst)) acc) (rest lst))]))

(define (tree-map func lst)
  (if (empty? lst) lst (reverse(helper func '() lst))))

(tree-map add1 '())
(tree-map add1 '(1 2 3))
(define a (tree-map (lambda (x) (modulo x 2))
                          '((1 2) (3 4) 5 (6 (7)))))
(define b '((1 2) (3 4) 5 (6 (7))))
(tree-map (lambda (x) (modulo x 2))
                          '((1 2) (3 4) 5 (6 (7))))

(module+ test
  (require rackunit)
  (check-equal? (tree-map add1 '()) '())
  (check-equal? (tree-map add1 '(1 2 3)) '(2 3 4))
  (check-equal? (tree-map (lambda (x) (* x x)) '(1 2 3)) '(1 4 9))
  (check-equal? (tree-map sub1 '(1 (2 3))) '(0 (1 2)))
  (check-equal? (tree-map (lambda (x) (modulo x 2))
                          '((1 2) (3 4) 5 (6 (7))))
                '((1 0) (1 0) 1 (0 (1))))
  (check-equal? (tree-map (lambda (x)
                            (string-append "I wanna " x))
                          '("pony" ("xbox" "A+")))
                '("I wanna pony" ("I wanna xbox" "I wanna A+"))))