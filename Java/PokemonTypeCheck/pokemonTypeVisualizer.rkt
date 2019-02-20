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

; currPokemonTypes takes in a pokemon name in
; string format, and returns the types asscoiated
; with that pokemon, an error message will be
; returned if the pokemon is not valid
(define (currPokemonTypes pokemon)
  (let* ([allNames (getAllNames)])
    (if (isMember pokemon allNames)
        (removeAll " " (map (lambda (x)
         (if (equal? (hash-ref (hash-ref x 'name) 'english) pokemon)
             (hash-ref x 'type) " ")) readFile)) '("Invalid Pokemon"))))

(module+ test
  (require rackunit)
  (check-equal? (currPokemonTypes "Pickachu") '("Invalid Pokemon"))
  (check-equal? (currPokemonTypes "Gengar") '("Ghost" "Poison")))

; removeAll takes a string and a list and removes all
; occurences of the string from the list of strings.
; used for removing spaces from currPokemonTypes return
; value. 
(define (removeAll sym lst)
  (define (helper sym lst acc)
    (cond
      [(empty? lst) acc]
      [else
       (if (equal? sym (first lst))
           (helper sym (rest lst) acc)
           (helper sym (rest lst) (append acc (first lst))))]))
    (helper sym lst empty))

(define (currPokemonStrAtk pokemon)
  (let* ([currTypes (currPokemonTypes pokemon)])
    (if (equal? "Invalid Pokemon" (first currTypes))
        (error 'currPokemonStrAtk "Error Invalid Pokemon")
        (sort (remove-duplicates (flatten (map (lambda (type)
               (removeAll " "
                          (map (lambda (x)
                                 (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                                     (hash-ref (hash-ref x 'typeEffective) 'strongAtk) " ")) typesFile))) currTypes))) string<?))))

(define (currPokemonStrDef pokemon)
  (let* ([currTypes (currPokemonTypes pokemon)])
    (if (equal? "Invalid Pokemon" (first currTypes))
        (error 'currPokemonStrAtk "Error Invalid Pokemon")
        (sort (remove-duplicates (flatten (map (lambda (type)
               (removeAll " "
                          (map (lambda (x)
                                 (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                                     (hash-ref (hash-ref x 'typeEffective) 'strongDef) " ")) typesFile))) currTypes))) string<?))))

(define (currPokemonNoEffect pokemon)
  (let* ([currTypes (currPokemonTypes pokemon)])
    (if (equal? "Invalid Pokemon" (first currTypes))
        (error 'currPokemonStrAtk "Error Invalid Pokemon")
        (sort (remove-duplicates (flatten (map (lambda (type)
               (removeAll " "
                          (map (lambda (x)
                                 (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                                     (hash-ref (hash-ref x 'typeEffective) 'noEffect) " ")) typesFile))) currTypes))) string<?))))

(define (gatherTypeInfo pokemon)
  (let* ([strAtk (currPokemonStrAtk pokemon)]
         [strDef (currPokemonStrDef pokemon)]
         [noEffect (currPokemonNoEffect pokemon)]
         [type (currPokemonTypes pokemon)])
    (hasheq "type" type "noEffect" noEffect "strAtk" strAtk "strDef" strDef "name" pokemon)))

(module+ test
  (require rackunit)
  (check-equal? (gatherTypeInfo "Charmander")
   '#hasheq(("type" . ("Fire"))
         ("strDef" . ("Bug" "Fairy" "Fire" "Grass" "Ice" "Steel"))
         ("noEffect" . ())
         ("name" . "Charmander")
         ("strAtk" . ("Bug" "Grass" "Ice" "Steel"))))
  (check-equal? (gatherTypeInfo "Gengar")
                '#hasheq(("type" . ("Ghost" "Poison"))
         ("strDef" . ("Bug" "Fairy" "Fighting" "Grass" "Poison"))
         ("noEffect" . ("Normal"))
         ("name" . "Gengar")
         ("strAtk" . ("Ghost" "Grass" "Poison" "Psychic")))))

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

; returns the types of the given pokemon name
;(define (pokemonTypes name)
;  (if (isMember name )))

;(visualize-json-file file1)
(define (a)
(for ([i (build-list (length readFile) values)]) (if (odd? i) (number->string i) "not odd")))

#|(define (typeStrAttacking type)
  (define (helper type acc)
    (cond
      [(empty? type) acc]
      [else
       (sort
        (flatten
         (helper (rest type)
                 (map (lambda (x)
                        (if (equal? (hash-ref (hash-ref x 'languages) 'english) (first type))
                            (append acc (hash-ref (hash-ref x 'typeEffective) 'strongAtk))
                            acc)) typesFile))) string<?)]))
  (helper type empty))|#

; typeStrAttacking takes in a type as a string
; and returns a list of all types the given
; type has a strong attack against
(define (typeStrAttacking type)
  (define (helper type acc)
    (sort
     (flatten
      (map (lambda (x)
             (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                 (append acc (hash-ref (hash-ref x 'typeEffective) 'strongAtk))
                 acc)) typesFile)) string<?))
  (helper type empty))

(module+ test
  (require rackunit)
  (check-equal? (typeStrAttacking "Fighting") '("Dark" "Ice" "Normal" "Rock" "Steel")))

(define (typeNoEffectAgainst moveType)
  (define (helper type acc)
    (sort
     (flatten
      (map (lambda (x)
             (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                 (append acc (hash-ref (hash-ref x 'typeEffective) 'noEffect))
                 acc)) typesFile)) string<?))
  (helper moveType empty))

(define (strAtkHelper type moveStrAttack)
  (define (helper type moveStrAttack acc)
    (cond
      [(empty? type) acc]
      [else (helper (rest type) moveStrAttack (cons (cons? (member (first type) moveStrAttack)) acc))]))
  (helper type moveStrAttack empty))
  ;(flatten (foldl (lambda (x y) (cons y (member x moveStrAttack))) empty type)))

(define (boolsEvaluator lst)
  (define (helper lst acc)
    (cond
      [(empty? lst) acc]
      [else (helper (rest lst) (or acc (first lst)))]))
  (helper lst #f))

(define (boolsAdjust lst)
  (define (helper lst acc)
    (cond
      [(empty? lst) acc]
      [else (helper (rest lst) (if (first lst) (* acc 2) acc))]))
  (helper lst 1))

(define (moveEffectiveness moveType pokemon)
  (let ([E 1])
    (let* ([pokemonTypeInfo (hash->list (gatherTypeInfo pokemon))])
      (let* ([pokemonStrDef (second pokemonTypeInfo)]
             [moveStrAttack (typeStrAttacking moveType)]
             [noEffect (typeNoEffectAgainst moveType)]
             [type (first pokemonTypeInfo)])
        (if (cons? noEffect)
            (if (foldl (lambda (x y) (or y (cons? (member x noEffect)))) #f type) (set! E (* E 0)) E) E)
        (if (cons? (member moveType pokemonStrDef)) (set! E
                                                          (let* ([res (* E 0.5)])
                                                            (if (equal? 0 (modulo (* 2 res) 2)) (truncate res) (rationalize res 0)))) E)
        (let* ([bools (strAtkHelper type moveStrAttack)])
          (if (boolsEvaluator bools) (set! E (* E (boolsAdjust bools))) E))))
    E))

(module+ test
  (require rackunit)
  ;(gatherTypeInfo "Raticate")
  ; ghost vs normal == 0
  (check-equal? (moveEffectiveness "Ghost" "Raticate") 0)
  ; electric vs ground == 0
  (check-equal? (moveEffectiveness "Electric" "Sandslash") 0)
  ; electric vs flying == 2
  (check-equal? (moveEffectiveness "Electric" "Pidgeot") 2)
  ; fire vs water == 0.5
  (check-equal? (moveEffectiveness "Fire" "Squirtle") 0.5)
  (check-equal? (moveEffectiveness "Fire" "Snover") 4)
  (check-equal? (moveEffectiveness "Psychic" "Croagunk") 4)
  (check-equal? (moveEffectiveness "Fire" "Empoleon") 1)
  (check-equal? (moveEffectiveness "Fighting" "Crobat") 0.25))