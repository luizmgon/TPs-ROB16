(define (domain SINGES)
  (:requirements :strips)
  (:predicates (caissePos ?cpos)
               (singePos ?spos)
               (bananaPos ?bpos)
               (haut)
	       (bas)
               (holding)
	       (notHolding))

  (:action aller
           :parameters (?from ?to)
           :precondition (and (singePos ?from) (bas))
           :effect (and (not (singePos ?from)) (singePos ?to)))

  (:action pousser
           :parameters (?from ?to)
           :precondition (and (caissePos ?from)(singePos ?from)(bas))
           :effect (and (not (caissePos ?from)) (caissePos ?to)
                        (not (singePos ?from)) (singePos ?to)))

  (:action monter
           :parameters (?pos)
           :precondition (and (caissePos ?pos)(singePos ?pos) (bas))
           :effect (and (haut) (not(bas))))

  (:action descendre
           :precondition (haut)
           :effect (and (not(haut)) (bas)))

  (:action attraper
           :parameters (?pos)
           :precondition (and (singePos ?pos) (bananaPos ?pos) (haut) (notHolding))
           :effect (and (not(notHolding)) (holding)))

  (:action lacher
           :precondition (holding)
           :effect (and(not (holding)) (notHolding))))
