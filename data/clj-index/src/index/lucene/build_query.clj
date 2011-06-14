(ns index.lucene.build-query
  (:import (org.apache.lucene.index Term)
    (org.apache.lucene.search BooleanClause$Occur BooleanQuery TermQuery)))

(defn get-occur-type [kwd]
  (cond
    (= kwd :and) (BooleanClause$Occur/MUST)
    (= kwd :not) (BooleanClause$Occur/MUST_NOT)
    (= kwd :or)  (BooleanClause$Occur/SHOULD)
    :else        (throw (Exception.
                          (str "Not a valid occurrence (" (name kwd) ").")))))

(defn create-term-query [v]
  (-> (Term. "_default" v) (TermQuery.)))

(defn build-query [q-lst]
  (let [query   (BooleanQuery.)
        indices (range 0 (count q-lst) 2)]
    (doseq [i indices]
      (let [term        (nth q-lst (inc i))
            kwd         (keyword (nth q-lst i))
            term-query  (create-term-query term)
            occur       (get-occur-type kwd)]
        (. query add term-query occur)))))

(defn -main [& args]
  (let [query [:and "ken" :or "pu"]]
    (build-query query)))
