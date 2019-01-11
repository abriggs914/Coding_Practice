#lang racket

(define (top-three lst)
  (let [(lst2 (sort lst >))]
  (cons (first lst2) (cons (second lst2) (cons (third lst2) empty)))))

(define (rand-list size max)
  (define (helper size max lst)
    (cond
      [(zero? size) lst]
      [else (let [(x (ceiling (* max (random))))]
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

(top-three (list 1 5 4 8 6 7 5 1 2 300))
(define a (rand-list 10 10))
(define b (rand-list 100 1000))

(equal? a b)

(top-three a)
(top-three b)
(top-n 5 b)
(bottom-n 5 b)