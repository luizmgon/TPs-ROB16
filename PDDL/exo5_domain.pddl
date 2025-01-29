(define (domain NOEUDS)
  (:requirements :strips)
  (:predicates (arc ?from ?to)
	       (agentPos ?from)
	       )

  (:action avancer
	     :parameters (?from ?to)
	     :precondition (and (arc ?from ?to) (agentPos ?from))
    	     :effect (and (not (agentPos ?from)) (agentPos ?to))))
