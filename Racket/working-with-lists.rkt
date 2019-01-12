#lang racket

(define (top-three lst)
  (let [(lst2 (sort lst >))]
  (cons (first lst2) (cons (second lst2) (cons (third lst2) empty)))))

(define (rand-list size max)
  (define (helper size max lst)
    (cond
      [(zero? size) lst]
      [else (let [(x (floor (* (+ 1 max) (random))))]
              (helper (- size 1) max (cons x lst)))]))
  (helper size max empty))

(define (top-n n lst)
  (define (helper c n lst acc)
    (let [(x (sort lst >))]
      (cond
        [(or (empty? x) (>= c n)) acc]
        [else (helper (add1 c) n (rest x) (cons (first x) acc))])))
  (sort (helper 0 n lst empty) >))


(define (bottom-n n lst)
  (define (helper c n lst acc)
    (let [(x (sort lst <))]
      (cond
        [(or (empty? x) (>= c n)) acc]
        [else (helper (add1 c) n (rest x) (cons (first x) acc))])))
  (sort (helper 0 n lst empty) <))

" -- Top three list -- "
(top-three (list 1 5 4 8 6 7 5 1 2 300))
(define a1 (rand-list 10 10))
(define b1 (rand-list 100 1000))

(module+ test
  (require rackunit)
  (check-not-equal? a1 b1))

" -- Top three a1 -- "
(top-three a1)
" -- Top three b1 -- "
(top-three b1)
" -- Top n=5 b1 -- "
(top-n 5 b1)
" -- Bottom n=3 b1 -- "
(bottom-n 5 b1)

(define x (list 1 2 3 4 5 22 11 020))
(define y (list 1.000 2 3 4 5 5 54 12 21 15 77 14 5 6 3 22 5 4 77 4 5 2 11 01 2 20))

(define lst (remove* x y =))

(define (remove-items items lst)
  (remove* items lst =))

(define a2 (list 1 2 3 4 5 6 7 8 9 10))
(define evens (list 0 2 4 6 8 10))

(define b2 (rand-list 50 25))

(define my (remove-items evens a2))
(define rem (remove* evens a2 eqv?))
;(equal? my rem)

(module+ test
  (require rackunit)
  (check-equal? my rem))