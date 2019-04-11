#lang racket
(provide baseConverter number->list list->number)

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

 --Apr 2019--

 Added hexadecimal functionality,
 allowing use of chars (A-F / a-f)
 to be converted to numbers. Must
 be a list if more than one digit
 given.
|#

; Takes in a number and a base.
; converts the number to it's
; corresponding base 10 value.
(define (baseTenConverter n b)
  (define (helper n b acc)
    (let ([res (modulo n b)])
      (cond
        [(>= 0 n) acc]
        [else (helper (floor (/ n b)) b (cons res acc))])))
  (helper n b empty))

; Takes in a number and returns
; each digit separately listed
(define (number->list n)
  (let ([n
         (map
          (lambda (x) (- (char->integer x) 48))
          (reverse (string->list (number->string n))))])
    (reverse n)))

; Takes in a list and returns a
; number by summing each element
; after multiplying by place value.
(define (list->number lst)
  (define (helper lst n i)
    (cond
      [(empty? lst) n]
      [else (helper (rest lst) (+ n (* (first lst) (expt 10 i))) (add1 i))]))
  (helper (reverse lst) 0 0))

; Takes a number the current number's
; base, and the desired resultant base.
; Can take a list of numbers as well
(define (baseConverter n cb rb)
  (if (and (> cb 0) (> rb 0))
      (let* ([x (verify n cb)]
             [n (reverse (number->list x))]
             [cb (if (and (= 16 cb) (list? n)) 10 cb)])
        (define (helper n cb acc i)
          (cond
            [(empty? n) acc]
            [(< x cb) x]
            [else (helper (rest n) cb (+ acc (* (first n) (expt cb i))) (add1 i))]))
        (baseTenConverter (helper n cb 0 0) rb))
      (error 'baseConverter "Invalid base given")))

; Takes a list of digits the current
; base, an accumulator, and a count.
; recursively calls baseConverter and
; adds the sum in order and weighted
; according to place value.
(define (fun n cb acc i)
  (cond
    [(empty? n) acc]
    [else
     (let ([a (first n)]
           [b i])     
     (fun (rest n) cb
               (+ acc (* (expt cb i)
                         (list->number (baseConverter (first n) cb 10))))
               (add1 i)))]))

; Takes in a number/list/char and returns
; it's numerical equivalent.
(define (verify n cb)
  (cond
    [(number? n) n]
    [(list? n) (fun (reverse n) cb 0 0)]
    [(char? n)
     (let* ([x (char->integer n)]
            [x (if (> x 70) (- x 32) x)])
       (cond
         [(= x 65) 10] ; A
         [(= x 66) 11] ; B
         [(= x 67) 12] ; C
         [(= x 68) 13] ; D
         [(= x 69) 14] ; E
         [(= x 70) 15] ; F
         [else (error 'verify "Invalid letter")]))]
    [else (error 'verify "Invalid number given")]))

(module+ test
  (require rackunit)
  (define-syntax-rule (check-fail expr)
    (check-exn exn:fail? (lambda () expr)))
  
  (check-equal? (baseTenConverter 17 2)
                '(1 0 0 0 1))
  (check-equal? (baseTenConverter 50 8)
                '(6 2))

  (check-equal? (number->list 10001)
                '(1 0 0 0 1))
  (check-equal? (number->list 62)
                '(6 2))
  
  (check-equal? (baseConverter 10001 2 10)
                '(1 7))
  (check-equal? (baseConverter 62 8 2)
                '(1 1 0 0 1 0))
  (check-equal? (baseConverter 248712225 10 2)
                '(1 1 1 0 1 1 0 1 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0 1))
  
  (check-equal? (list->number '(1 1 1 0 1 1 0 1 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0 1))
                1110110100110000110000100001)
  (check-equal? (list->number (baseConverter 1110110100110000110000100001 2 10))
                248712225)
  (check-equal? (list->number (baseConverter (list->number '(1 0 7 7 6 5 1 5 2 0)) 10 2))
                1000000001110111010100001000000)
  
  (check-equal? (list->number (baseConverter #\F 16 10))
                15)
  (check-equal? (list->number (baseConverter '(1 #\F) 16 10))
                31)
  (check-equal? (list->number (baseConverter '(5 0 5 0 5 0) 16 10))
                5263440)
  (check-equal? (list->number (baseConverter '(#\A #\B #\C #\D #\E #\F) 16 10))
                11259375)
  (check-equal? (list->number (baseConverter '(1 0) 2 10))
                2)
  (check-fail (list->number (baseConverter '(#\A #\B #\C #\D #\E #\H) 16 10)))
  (check-fail (list->number (baseConverter '('(#\A)) 16 10)))
  (check-fail (list->number (list->number (baseConverter '(1 0) -2 10)))))