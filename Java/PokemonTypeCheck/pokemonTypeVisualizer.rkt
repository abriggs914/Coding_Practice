#lang racket
(require json)
(require explorer)

(define file1 "./full_pokedex.json")
(define file2 "./pokemonTypes.json")

(define (read-json-file file-name)
      (with-input-from-file file-name read-json))

;; The parsed pokedex json file in hasheq form
;; lists all pokemon and data
(define readFile (read-json-file file1))


;; The parsed types json file in hasheq form
;; lists all pokemon and data
(define typesFile (read-json-file file2))

(define (visualize-json-file file-name)
      (explore (read-json-file file-name)))

(define (currPokemonTypes pokemon)
  (let* ([allNames (getAllNames)])
    (if (isMember pokemon allNames)
        (removeAll "" (map (lambda (x)
         (if (equal? (hash-ref (hash-ref x 'name) 'english) pokemon)
             (hash-ref x 'type) "")) readFile)) "Invalid Pokemon")))
  ;(hash-ref (hash-ref readFile 'name) 'english))

(define (removeAll sym lst)
  (map (remove sym lst) lst))

;(define (currPokemonStrAtk pokemon)
;  )

;;Returns a boolean value #t if the pokemon
;;is in the hasheq, #f if not
(define (isMember item lst)
  (let*
      ([item
          (cond
            [(symbol? item) (symbol->string item)]
            [(not (string? item)) #f]
            [else item])])
  (if (list? (member item lst)) #t #f)))

(define (getAllTypes)
  (map (lambda (x) (hash-ref x 'type)) readFile))

(define (getAllNames)
  (map (lambda (x) (hash-ref (hash-ref x 'name) 'english)) readFile))


;(visualize-json-file file1)
(define (a)
(for ([i (build-list (length readFile) values)]) (if (odd? i) (number->string i) "not odd")))