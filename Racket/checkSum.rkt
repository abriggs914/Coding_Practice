#lang racket
(require "numberConverter.rkt")

(define (numDigits n)
  (length (string->list (number->string n))))

(define (pad n)
  (build-list n (lambda (x) (* x 0))))

(define (checkSum lst chk)
  (define (helper lst acc)
    (cond
      [(empty? lst) acc]
      [else (helper (rest lst) (list->number (binAdd acc (first lst))))]))
  (let* ([sum (flip (number->list (helper lst 0)))]
         [comp (binAdd chk (list->number sum))]
         [l (length comp)]
         [identity (build-list l (lambda (x) (if (= x 0) 1 (/ x x))))])
    (display "\tSUM: ")
    (display sum)
    (display "\n")
    (if (foldl (lambda (x y) (and x y)) #t (map (lambda (x y) (= x y)) comp identity)) #t #f)))

(define (binAdd a b)
  (let* ([listA (baseConverter a 2 10)]
         [listB (baseConverter b 2 10)]
         [lengthA (length listA)]
         [lengthB (length listB)])
    (cond
      [(< lengthA lengthB) (set! listA (append (pad (- lengthB lengthA)) listA))]
      [(> lengthA lengthB) (set! listB (append (pad (- lengthA lengthB)) listB))])
    (baseConverter (list->number (map (lambda (x y) (+ x y)) listA listB)) 10 2)))

(define (flip lst)
  (map (lambda (x) (if (= 0 x) 1 0)) lst))


(binAdd 101 1110001)
(binAdd 101 101110000)
(checkSum '(101 1110001) 1110110)

(module+ test
  (require rackunit)
  (check-equal? (file-exists? "C:/Users/abrig/OneDrive/Documents/Coding Practice/Coding_Practice/Racket/numberConverter.rkt") #t)
  (check-equal? (checkSum '(101 1110001) 1110110) #t)
  (check-equal? (checkSum '(101 1110001) 1110111) #f)
  (check-equal? (flip (binAdd 101 1110001)) '(0 0 0 1 0 0 1))
  (check-equal? (numDigits 1546) 4)
  (check-equal? (checkSum '(1 100 1011 111101 11101 1011 11111011 111) 10010001) #f)
  (check-equal? (checkSum '(1 100 1011 111101 11101 1011 11111011 111) 101110111) #t))