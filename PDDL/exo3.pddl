(define (problem BLOCKS-TOUR)
(:domain BLOCKS)
(:objects D B A C )
(:INIT (CLEAR B) (ON B C) (ON C A) (ON A D) (ONTABLE D) (HANDEMPTY))
(:goal (AND (ON D C) (ON C A) (ON A B)))
)
