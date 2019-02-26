#lang racket

#|
 Pokemon type effectiveness evaluator.
 February 2019
 Avery Briggs
|#

(require json)
(require explorer)
(require math)

(define file1 "./full_pokedex.json")
(define file2 "./pokemonTypes.json")

(define (read-json-file file-name)
      (with-input-from-file file-name read-json))

(define (visualize-json-file file-name)
      (explore (read-json-file file-name)))

;; The parsed pokedex json file in hasheq form
;; lists all pokemon and data.
(define readFile (read-json-file file1))


;; The parsed types json file in hasheq form
;; lists all pokemon and data.
(define typesFile (read-json-file file2))

; getAllTypes returns a list of all types in
; the fullPokedex.json file.
(define (getAllTypes)
  (map (lambda (x) (hash-ref x 'type)) readFile))

; getAllNames returns a list of all names in
; the fullPokedex.json file.
(define (getAllNames)
  (map (lambda (x) (hash-ref (hash-ref x 'name) 'english)) readFile))

;;Returns a boolean value #t if the pokemon
;;is in the hasheq, #f if not.
(define (isMember item lst)
  (let*
      ([item
          (cond
            [(symbol? item) (symbol->string item)]
            [(not (string? item)) #f]
            [else item])])
  (if (list? (member item lst)) #t #f)))

; currPokemonTypes takes in a pokemon name in
; string format, and returns the types asscoiated
; with that pokemon, an error message will be
; returned if the pokemon is not valid.
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

; currPokemonStrAtk takes in a pokemon name string
; and returns a list of sorted unique types that the
; given pokemon has a type advantage over when attacking
; that type (Effectiveness = 2.0 dealt).
(define (currPokemonStrAtk pokemon)
  (let* ([currTypes (currPokemonTypes pokemon)])
    (if (equal? "Invalid Pokemon" (first currTypes))
        (error 'currPokemonStrAtk "Error Invalid Pokemon")
        (sort (remove-duplicates (flatten (map (lambda (type)
               (removeAll " "
                          (map (lambda (x)
                                 (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                                     (hash-ref (hash-ref x 'typeEffective) 'strongAtk) " ")) typesFile))) currTypes))) string<?))))

; currPokemonStrDef takes in a pokemon name string
; and returns a list of sorted types that the given
; pokemon has a type advantage over when defending
; that type (Effectiveness = 0.5 recieved).
(define (currPokemonStrDef pokemon)
  (let* ([currTypes (currPokemonTypes pokemon)])
    (if (equal? "Invalid Pokemon" (first currTypes))
        (error 'currPokemonStrAtk "Error Invalid Pokemon")
        (sort (flatten (map (lambda (type)
               (removeAll " "
                          (map (lambda (x)
                                 (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                                     (hash-ref (hash-ref x 'typeEffective) 'strongDef) " ")) typesFile))) currTypes)) string<?))))

; currPokemonNoEffect takes in a pokemon name string
; and returns a list of sorted unique types that
; given pokemon has no type Effect when attacking
; that type (Effectiveness = 0.0 dealt).
(define (currPokemonNoEffect pokemon)
  (let* ([currTypes (currPokemonTypes pokemon)])
    (if (equal? "Invalid Pokemon" (first currTypes))
        (error 'currPokemonStrAtk "Error Invalid Pokemon")
        (sort (remove-duplicates (flatten (map (lambda (type)
               (removeAll " "
                          (map (lambda (x)
                                 (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                                     (hash-ref (hash-ref x 'typeEffective) 'noEffect) " ")) typesFile))) currTypes))) string<?))))

; gathrTypeInfo takes in a pokemons name string
; and returns a hasheq of that pokemons:
; noEffect
; name
; type 
; strAttack
; strDef
; all values are lists of strings and should be
; accessed using string indexing after calling
; hash->licst on the resulting hasheq.
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
         ("strDef" . ("Bug" "Bug" "Fairy" "Fighting" "Grass" "Poison" "Poison"))
         ("noEffect" . ("Normal"))
         ("name" . "Gengar")
         ("strAtk" . ("Ghost" "Grass" "Poison" "Psychic")))))

; getAttribute takes in a hasheq, meant for the
; resulting call of gatherTypeInfo, and an attribute
; as a string (one of: "name","type","strAtk","strDef","noEffect").
; returns the value asscoiated with the attribute given.
(define (getAttribute info att)
  (let ([info (hash->list info)])
    (cdr (first (filter (lambda (x) (equal? att (car x))) info)))))

(module+ test
  (require rackunit)
  (check-equal? (getAttribute (gatherTypeInfo "Charmander") "name") "Charmander")
  (check-equal? (getAttribute (gatherTypeInfo "Charmander") "type") '("Fire"))
  (check-equal? (getAttribute (gatherTypeInfo "Charmander") "noEffect") '())
  (check-equal? (getAttribute (gatherTypeInfo "Charmander") "strAtk") '("Bug" "Grass" "Ice" "Steel"))
  (check-equal? (getAttribute (gatherTypeInfo "Charmander") "strDef") '("Bug" "Fairy" "Fire" "Grass" "Ice" "Steel")))

; returns the types of the given pokemon name
;(define (pokemonTypes name)
;  (if (isMember name )))

;(visualize-json-file file1)
;(define (a)
;(for ([i (build-list (length readFile) values)]) (if (odd? i) (number->string i) "not odd")))

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
; type has a strong attack against.
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

; noeEffectAgainst takes in a type string and
; returns a list of all types that type has
; no effect against.
(define (typeNoEffectAgainst moveType)
  (define (helper type acc)
    (sort
     (flatten
      (map (lambda (x)
             (if (equal? (hash-ref (hash-ref x 'languages) 'english) type)
                 (append acc (hash-ref (hash-ref x 'typeEffective) 'noEffect))
                 acc)) typesFile)) string<?))
  (helper moveType empty))

; strAttackHelper is a helper method to moveEffectiveness
; it takes in a list of types for the defending pokemon
; and a list of types that the attacking pokemon has a
; type advantage over. Returns a list of booleans for each
; defending type if it is found on the attacking advantage
; list. results are combined with bools evaluator to determine
; if the match-up is super effective.
(define (strAtkHelper type moveStrAttack)
  (define (helper type moveStrAttack acc)
    (cond
      [(empty? type) acc]
      [else (helper (rest type) moveStrAttack (cons (cons? (member (first type) moveStrAttack)) acc))]))
  (helper type moveStrAttack empty))

; occur counts the number of occurences of a particular
; item, exist in a given list. Returns a number count.
(define occur
  (lambda (a s)
    (count (curry equal? a) s)))

; strDefHelper is a helper method to moveEffectiveness
; it takes in a the type of the attacking pokemon move
; and a list of types that the  for the defending pokemon
; has a type advantage over. Returns a number based on the
; calculated effectiveness for that move on the defending
; pokemon.
(define (strDefHelper type pokemonStrDef)
  (expt 0.5 (occur type pokemonStrDef)))

; boolsEvaluator takes in a list of booleans
; and takes the logical or of each element.
(define (boolsEvaluator lst)
  (define (helper lst acc)
    (cond
      [(empty? lst) acc]
      [else (helper (rest lst) (or acc (first lst)))]))
  (helper lst #f))

; boolsAdjust takes in a list of booleans and
; returns a multiple of 2 based on how many #t
; values are found.
(define (boolsAdjust lst)
  (define (helper lst acc)
    (cond
      [(empty? lst) acc]
      [else (helper (rest lst) (if (first lst) (* acc 2) acc))]))
  (helper lst 1))

; moveEffectiveness takes in an attacking move type string and a
; defending pokemon name string. Returns the calculated effectiveness
; of that attacking move on the defending pokemon (0,0.25,0.5,1,2,4).
(define (moveEffectiveness moveType pokemon)
  (let ([E 1.0])
    (let* ([pokemonTypeInfo (gatherTypeInfo pokemon)])
      (let* ([pokemonStrDef (getAttribute pokemonTypeInfo "strDef")]
             [moveStrAttack (typeStrAttacking moveType)]
             [noEffect (typeNoEffectAgainst moveType)]
             [type (getAttribute pokemonTypeInfo "type")])
        (if (cons? noEffect)
            (if (foldl (lambda (x y) (or y (cons? (member x noEffect)))) #f type) (set! E (* E 0.0)) E) E)
        (let* ([mult (strDefHelper moveType pokemonStrDef)])
          (set! E (* E mult)))
        (let* ([bools (strAtkHelper type moveStrAttack)])
          (if (boolsEvaluator bools) (set! E (* E (boolsAdjust bools))) E))))
    E))

(module+ test
  (require rackunit)
  ; ghost vs normal == 0.0
  (check-equal? (moveEffectiveness "Ghost" "Raticate") 0.0)
  ; electric vs ground == 0.0
  (check-equal? (moveEffectiveness "Electric" "Sandslash") 0.0)
  ; electric vs flying == 2.0
  (check-equal? (moveEffectiveness "Electric" "Pidgeot") 2.0)
  ; fire vs water == 0.5
  (check-equal? (moveEffectiveness "Fire" "Squirtle") 0.5)
  ; fire vs grass ice == 4.0
  (check-equal? (moveEffectiveness "Fire" "Snover") 4.0)
  ; psychic vs poison fighting == 4.0
  (check-equal? (moveEffectiveness "Psychic" "Croagunk") 4.0)
  ; fire vs steel water == 1.0
  (check-equal? (moveEffectiveness "Fire" "Empoleon") 1.0)
  ; fighting vs flying poison == 0.25
  (check-equal? (moveEffectiveness "Fighting" "Crobat") 0.25))

; convertNum takes in a number value and returns the
; equivalent number in natural form (no decimals, max: 809).
(define (convertNum n)
  (define (helper n i)
      (cond
        [(= n i) i]
        [(> i (length readFile)) (error 'convertNum "Invalid number given")]
        [else (helper n (add1 i))]))
  (helper n 0))

; genTeam will randomly generate a team of six pokemon
; returns a list of hasheqs (result of gatherTypeInfo).
(define (genTeam)
  (define (helper team members)
    (cond
      [(= 6 members) team]
      [else (helper
             (cons (gatherTypeInfo
                    (hash-ref (hash-ref
                               (list-ref readFile (convertNum (floor (* (random) (length readFile)))))
                               'name) 'english)) team) (add1 members))]))
  (helper empty 0))

; bestTeamDefender takes in a list of pokemon considered
; a team, and an attacking move type. Returns the best
; pokemon to defend against the move type as a hasheq.
; (typically effectiveness recieved == 0 || 0.5 || 1).
(define (bestTeamDefender team moveType)
  (define (helper team moveType bestChoice)
    (cond
      [(empty? team) bestChoice]
      [else (helper (rest team) moveType (if (> (moveEffectiveness moveType (getAttribute (first team) "name"))
                                                (moveEffectiveness moveType (getAttribute bestChoice "name")))
                                             bestChoice (first team)))]))
  (helper (rest team) moveType (first team)))


; worstTeamDefender takes in a list of pokemon considered
; a team, and an attacking move type. Returns the worst
; pokemon to defend against the move type as a hasheq.
; (typically effectiveness recieved == 1 || 2 || 4).
(define (worstTeamDefender team moveType)
  (define (helper team moveType bestChoice)
    (cond
      [(empty? team) bestChoice]
      [else (helper (rest team) moveType (if (< (moveEffectiveness moveType (getAttribute (first team) "name"))
                                                (moveEffectiveness moveType (getAttribute bestChoice "name")))
                                             bestChoice (first team)))]))
  (helper (rest team) moveType (first team)))

; getTypeListNames returns a list of all pokemon
; types as strings.
(define (getTypeListNames)
  (map (lambda (type) (hash-ref (hash-ref type 'languages) 'english )) typesFile))

; genGivenTeam takes in a list of strings corresponding
; to pokemon names, and returns a list of hasheqs resulting
; from the gatherTypeInfo method.
(define (genGivenTeam lst)
  (let* ([bool (foldl (lambda (x y) (and (isMember x (getAllNames)) y)) #t lst)])
    (if bool (map (lambda (x) (gatherTypeInfo x)) lst) (error 'genGivenTeam "Invalid team given"))))

; teamEffectivenessPerType takes in a list of hasheqs repesenting
; a team. Displays and returns a table of all types and each pokemon's
; effectiveness recieved when defending against each type column in
; the table.
(define (teamEffectivenessPerType team)
  (display " ((NRM FGT FLY PSN GRD RCK BUG GST STL FIR WTR GRS ELC PSY ICE DRG DRK FRY)\n")
  (map
   (lambda (member)
     (map (lambda (type)
            (moveEffectiveness type (getAttribute member "name")))
          (getTypeListNames)))
   team))

(define b (genTeam))
(define moveType "Electric")
(bestTeamDefender b moveType)
(worstTeamDefender b moveType)
(define pearlTeamList '("Infernape" "Gengar" "Luxray" "Gyarados" "Garchomp" "Alakazam"))


(define (reportTeamMoveVote team move)
   (let* ([teamEffectiveness
           (map (lambda (x)
                  (cons (getAttribute x "name")
                        (moveEffectiveness move (getAttribute x "name")))) team)]
          [bestCandidate (bestTeamDefender team move)]
          [worstCandidate (worstTeamDefender team move)]
          [effect (lambda (x) (moveEffectiveness move(getAttribute x "name")))])
     (display "\n\t")
     (display move)
     (display " type move V.S. trainer's team:\n")
     (display teamEffectiveness)
     (display "\n\tBest pokemon to defend with: ")
     (display (effect bestCandidate))
     (display "\n")
     (display bestCandidate)
     (display "\n\tWorst pokemon to defend with: ")
     (display (effect worstCandidate))
     (display "\n")
     (display worstCandidate)
     (display "\n")))

(reportTeamMoveVote b moveType)
(teamEffectivenessPerType (genGivenTeam pearlTeamList))

(define (sum a lst)
  (foldl (lambda (x y) (+ y x)) a lst))
(define (overall lst)
  (map (lambda (x) (sum 0 x)) lst))

(module+ test
  (require rackunit)
  (check-equal? (overall (teamEffectivenessPerType (genGivenTeam pearlTeamList))) '(18.75 17.75 17.5 18.5 20.5 20.0)))

; *OPTIMISTIC*
(define (listAllPokemonMatchEffectiveness pokemon effectiveness)
  (let ([pokemon (getAttribute (gatherTypeInfo pokemon) "type")])
    (cond
      [(empty? pokemon) empty]
      [else
       (let* ([allPokemon readFile]
              [type (first pokemon)]
              [secondType (rest pokemon)])
         (flatten (filter (lambda (poke)
                   (= effectiveness (moveEffectiveness type (hash-ref (hash-ref poke 'name) 'english)))) allPokemon)))])))

(module+ test
  (require rackunit)
  (define pokemon "Charmander")
  (define lst '(0.0 0.25 0.5 1.0 2.0 4.0))
  (define a (map (lambda (x) (listAllPokemonMatchEffectiveness pokemon x)) lst))
  (check-equal? (foldl (lambda (x y) (+ y (length x))) 0 a) (length readFile)))