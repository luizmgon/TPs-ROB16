(define (domain HANOI)
  (:requirements :strips)
  (:predicates (largerThan ?x ?y)
               (handEmpty)
	       (isPic ?x)
	       (isDisque ?x)
	       (holding ?x)
	       (on ?x ?y)
	       (isEmpty ?pic)
	       (clear ?x)	
)    

  (:action enleverDuPic
           :parameters (?disque ?pic)
           :precondition (and (isPic ?pic) (on ?disque ?pic) (clear ?disque) (handEmpty))
           :effect (and (not (handEmpty)) (holding ?disque) (not(on ?disque ?pic)) (isEmpty ?pic)))

  (:action mettreSurPicVide
           :parameters (?disque ?pic)
           :precondition (and (isEmpty ?pic)(isPic ?pic)(holding ?disque))
           :effect (and (not (isEmpty ?pic)) (on ?disque ?pic) (not (holding ?disque)) (handEmpty)))

  (:action mettreSurDisque
           :parameters (?disque1 ?disque2)
           :precondition (and (holding ?disque1)(largerThan ?disque2 ?disque1)(clear ?disque2))
           :effect (and (on ?disque1 ?disque2) (not(holding ?disque1)) (handEmpty) (not(clear ?disque2)) ))

  (:action enleverDuDisque
	   :parameters (?disque1 ?disque2)
           :precondition (and (isDisque ?disque2) (on ?disque1 ?disque2) (handEmpty) (clear ?disque1))
           :effect (and (not (handEmpty)) (holding ?disque1) (not(on ?disque1 ?disque2)) (clear ?disque2)  ))

)
