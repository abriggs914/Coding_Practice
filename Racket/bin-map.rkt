#lang racket
#|
(define (binmap1 func lst1 lst2)
  (cond
    [(empty? lst1) lst2]
    [(empty? lst2) lst1]
    [(append (cons (func (first lst1) (first lst2)) '())  (binmap1 func (rest lst1) (rest lst2)))]))


(define (binmap2 func lst1 lst2)
  (cond
    [(empty? lst1) lst2]
    [(empty? lst2) lst1]
    [else (foldl (func (first lst1) (first lst2)) (binmap func (rest lst1) (rest lst2)) '())]))
|#

(define (helper acc func lsta lstb)
  (cond
    [(or (empty? lstb) (empty? lsta)) acc]
    [else (helper (cons (func (first lsta) (first lstb)) acc) func (rest lsta) (rest lstb))]))
  
(define (binmap func lst1 lst2)
  (cond
    [(empty? lst1) lst2]
    [(empty? lst2) lst1]
    [else (reverse (helper '() func lst1 lst2))]))

(module+ test
  (require rackunit)

  (check-equal? (binmap + '(1 2 3) '(4 5 6)) '(5 7 9))
  (check-equal? (binmap * '(1 2 3) '(4 5 6)) '(4 10 18))

  (check-equal? (binmap string-append '("hello" "world ")
                                      '(" mom" "travel"))
        '("hello mom" "world travel"))

  (check-equal? (binmap + '(1 2 3) '(4 5 6 7)) '(5 7 9))
  (check-equal? (binmap + '(1 2 3 4) '(4 5 6)) '(5 7 9))
  (check-equal? (binmap + '() '(4 5 6)) '(4 5 6))
  (check-equal? (binmap + '(1 2 3 4) '()) '(1 2 3 4)))