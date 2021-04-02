(declare-const x (Int))
(declare-const y (Int))

(assert (and (> x 0) (< x 10)))
(assert (and (> y 0) (< y 10)))
(assert (= (+ (* x x) 1) (- y 2)))

(check-sat)
(get-model)
(exit)
