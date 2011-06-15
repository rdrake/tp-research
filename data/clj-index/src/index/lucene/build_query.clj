(ns index.lucene.build-query
  (:import (org.apache.lucene.index Term)
           (org.apache.lucene.queryParser QueryParser)
           (org.apache.lucene.search BooleanClause$Occur
                                     BooleanQuery TermQuery)
           (org.apache.lucene.util Version))
  (:use [index.lucene :only [create-analyzer]]))

(defn get-occur-type [kwd]
  (cond
    (= kwd :and) (BooleanClause$Occur/MUST)
    (= kwd :not) (BooleanClause$Occur/MUST_NOT)
    (= kwd :or)  (BooleanClause$Occur/SHOULD)
    :else        (throw (Exception.
                          (str "Not a valid occurrence (" (name kwd) ").")))))

(defn create-term-query [qp term]
  (. qp parse term))

(defn build-query [q-lst]
  (let [query   (BooleanQuery.)
        indices (range 0 (count q-lst) 2)
        qp      (QueryParser. Version/LUCENE_32 "_default" (create-analyzer))]
    (doseq [i indices]
      (let [term        (nth q-lst (inc i))
            kwd         (keyword (nth q-lst i))
            term-query  (create-term-query qp term)
            occur       (get-occur-type kwd)]
        (. query add term-query occur)))
    query))

(defn -main [& args]
  (let [query [:and "KeN" :not "pu"]]
    (println (build-query query))))
