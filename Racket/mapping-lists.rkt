#lang plait
(define (func op a b)  
  (local [(define (helper acc op a b)
            (cond
              [(and (empty? a) (not (empty? b))) (helper (cons (op (first b) (first b)) acc) op a (rest b))]
              [(and (empty? b) (not (empty? a))) (helper (cons (op (first a) (first a)) acc) op (rest a) b)]
              [(and (empty? b) (empty? a)) acc]
              [else (helper (cons (op (first a) (first b)) acc) op (rest a) (rest b))]))]
    (reverse (helper '() op a b))))

(define a '(1 5 6 4 7))
(define b '(1 2 0 3 5))
(define c '(2 0 3 5))
(define d '("hey" "general"))
(define e '(" there" " kenobi"))
(func * a b)
(func * a c)
(func * b c)
(func * c a)
(func * c b)
(func * c c)
(func string-append d e)