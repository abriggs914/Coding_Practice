#lang racket

#|
 NumberConverter
 Feb 2019
 Avery Briggs
 3471065

 Simple number converter program.
 Converts any whole number to another
 number base. Also implements
 list->number and number->list
 methods to help conversion
|#

(define (baseTenConverter n b)
  (define (helper n b acc)
    (let ([res (modulo n b)])
      (cond
        [(>= 0 n) acc]
        [else (helper (floor (/ n b)) b (cons res acc))])))
  (helper n b empty))

(define (number->list n)
  (let ([n
         (map
          (lambda (x) (- (char->integer x) 48))
          (reverse (string->list (number->string n))))])
    (reverse n)))

(define (baseConverter n cb rb)
  (let ([n (reverse (number->list n))])
    (define (helper n cb acc i)
      (cond
        [(empty? n) acc]
        [else (helper (rest n) cb (+ acc (* (first n) (expt cb i))) (add1 i))]))
    (baseTenConverter (helper n cb 0 0) rb)))

(define (list->number lst)
  (define (helper lst n i)
    (cond
      [(empty? lst) n]
      [else (helper (rest lst) (+ n (* (first lst) (expt 10 i))) (add1 i))]))
  (helper (reverse lst) 0 0))

(module+ test
  (require rackunit)
  (check-equal? (baseTenConverter 17 2) '(1 0 0 0 1))
  (check-equal? (baseTenConverter 50 8) '(6 2))

  (check-equal? (number->list 10001) '(1 0 0 0 1))
  (check-equal? (number->list 62) '(6 2))
  
  (check-equal? (baseConverter 10001 2 10) '(1 7))
  (check-equal? (baseConverter 62 8 2) '(1 1 0 0 1 0))
  (check-equal? (baseConverter 248712225 10 2) '(1 1 1 0 1 1 0 1 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0 1))
  
  (check-equal? (list->number '(1 1 1 0 1 1 0 1 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0 1)) 1110110100110000110000100001)
  (check-equal? (list->number (baseConverter 1110110100110000110000100001 2 10)) 248712225))