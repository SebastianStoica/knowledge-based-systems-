
(defrule Verificare_COORD (declare (salience 3))
	(stare robot waiting)
	(coordonate finale X ?x Y ?y Z ?z)
	(test (not (and (numberp ?x) (numberp ?y) (numberp ?z))))
	=>
	(printout t "Introdu date validare !" crlf) 
)

(defrule Reintrare_Waiting (declare (salience -3))
	?a <- (deplasare efectuata)
	=>
	(retract ?a)
	(assert (stare robot waiting))
)

(defrule Prel_Obstacol
	(obstacol lungime: ?lungime latime: ?latime inaltime: ?inaltime centru X: ?x Y: ?y Z: ?z)
	(test (and (numberp ?x) (numberp ?y) (numberp ?z) (numberp ?inaltime) (numberp ?lungime) (numberp ?latime)))
	=>
	(printout t "Coordonate varfuri obstacol" crlf)
	(assert 
			(varf A X: (- ?x (/ ?lungime 2)) Y: (+ ?y (/ ?latime 2)) Z: ?z)
			(varf B X: (+ ?x (/ ?lungime 2)) Y: (+ ?y (/ ?latime 2)) Z: ?z)
			(varf C X: (+ ?x (/ ?lungime 2)) Y: (- ?y (/ ?latime 2)) Z: ?z)
			(varf D X: (- ?x (/ ?lungime 2)) Y: (- ?y (/ ?latime 2)) Z: ?z)
			(varf A' X: (- ?x (/ ?lungime 2)) Y: (+ ?y (/ ?latime 2)) Z: (+ ?z ?inaltime))
			(varf B' X: (+ ?x (/ ?lungime 2)) Y: (+ ?y (/ ?latime 2)) Z: (+ ?z ?inaltime))
			(varf C' X: (+ ?x (/ ?lungime 2)) Y: (- ?y (/ ?latime 2)) Z: (+ ?z ?inaltime))
			(varf D' X: (- ?x (/ ?lungime 2)) Y: (- ?y (/ ?latime 2)) Z: (+ ?z ?inaltime))
			(exista obstacol)
	)
)

(defrule Pct_admis_fara_obstacol
	?a <- (stare robot waiting)
	?b <- (coordonate finale X ?x Y ?y Z ?z)
	(test (and (numberp ?x) (numberp ?y) (numberp ?z)))
	(test (and (< ?x 0.5) (< ?y 0.5) (< ?z 0.5) (>= ?x -0.5) (>= ?y -0.5) (>= ?z 0)))
	(not (exista obstacol))
	=>
	(retract ?a)
	(assert (stare robot activa))
	(printout t "Punct admisibil. Se poate efectua deplasarea" crlf) 
)

(defrule Pct_inadmis_fara_obstacol
	?a <- (stare robot waiting)
	?b <- (coordonate finale X ?x Y ?y Z ?z)
	(test (not (and (numberp ?x) (numberp ?y) (numberp ?z))))
	(test (not (and (< ?x 0.5) (< ?y 0.5) (< ?z 0.5) (>= ?x -0.5) (>= ?y -0.5) (< ?z 0))))
	(not (exista obstacol))
	=>
	(retract ?a)
	(assert (stare robot activa))
	(printout t "Punct inadmisibil. In afara spatiului" crlf) 
)

(defrule Limite_obstacol 
	?a <- (varf A X: ?xa Y: ?ya Z: ?za)
	?b <- (varf B X: ?xb Y: ?yb Z: ?zb)
	?c <- (varf D X: ?xd Y: ?yd Z: ?zd)
	?d <- (varf A' X: ?xa' Y: ?ya' Z: ?za')
	(exista obstacol)
	=>
	(retract ?a ?b ?c ?d)
	(assert (limite x ?xa ?xb)
			(limite y ?yd ?ya)
			(limite z ?za ?za')
	)
)

(defrule Pct_admis_cu_obstacol 
	?a <- (stare robot waiting)
	(coordonate finale X ?x Y ?y Z ?z)
	;(test (and (numberp ?x) (numberp ?y) (numberp ?z)))
	;(test (and (< ?x 0.5) (< ?y 0.5) (< ?z 0.5) (>= ?x -0.5) (>= ?y -0.5) (>= ?z 0)))
	?b <- (limite x ?xinf ?xsup)
	?c <- (limite y ?yinf ?ysup)
	?d <- (limite z ?zinf ?zsup)
	?e <- (exista obstacol)
	(test (or 
				(or (> ?xinf ?x) (> ?x ?xsup))
				(or (> ?yinf ?y) (> ?y ?ysup))
				(or (> ?zinf ?z) (> ?z ?zsup))
		  )
	)
	=>
	(retract ?a ?b ?c ?d)
	(assert (stare robot activa))
	(printout t "Punct admisibil. Se poate efectua deplasarea" crlf) 
)

(defrule Pct_inadmis_cu_obstacol 
	?a <- (stare robot waiting)
	(coordonate finale X ?x Y ?y Z ?z)
	;(test (and (numberp ?x) (numberp ?y) (numberp ?z)))
	;(test (and (< ?x 0.5) (< ?y 0.5) (< ?z 0.5) (>= ?x -0.5) (>= ?y -0.5) (< ?z 0)))
	?b <- (limite x ?xinf ?xsup)
	?c <- (limite y ?yinf ?ysup)
	?d <- (limite z ?zinf ?zsup)
	?e <- (exista obstacol)
	(test (and 
	              (and (<= ?xinf ?x) (<= ?x ?xsup)) 
				  (and (<= ?yinf ?y) (<= ?y ?ysup)) 
				  (and (<= ?zinf ?z) (<= ?z ?zsup))
			)
	)
	=>
	(retract ?a ?b ?c ?d)
	(assert (stare robot activa))
	(printout t "Punct inadmisibil. Tinta se afla in obstacol sau in afara spatiului de lucru" crlf) 
)
        


