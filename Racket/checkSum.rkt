#lang racket
(require "numberConverter.rkt")

(define (numDigits n)
  (length (string->list (number->string n))))

(define (pad n)
  (build-list n (lambda (x) (* x 0))))

(define (checkSum lst chk)
  (let* ([sum (flip (foldl (lambda (x y) (binAdd x y)) (first lst) (rest lst)))]
         [comp (binAdd chk (list->number sum))]
         [l (length comp)]
         [identity (build-list l (lambda (x) (if (= x 0) 1 (/ x x))))])
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
  (check-equal? (numDigits 1546) 4))