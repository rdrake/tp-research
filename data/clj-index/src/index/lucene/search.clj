(ns index.lucene.search
  (:use [sandbox.lucene :only [create-query create-searcher create-reader]])
  (:use [clojure.contrib.seq :only [indexed]]))

(defn get-document [searcher doc-id]
  (-> (.document searcher doc-id) (.get "_default")))

(defn get-documents [searcher docs]
  (map #(get-document searcher (.doc %)) docs))

(defn -main [index-path & args]
  (let [searcher  (create-searcher index-path)
        reader    (create-reader index-path)
        query-str (apply str (interpose " " args))
        query     (create-query query-str)
        start     (System/currentTimeMillis)
        topdocs   (.search searcher query 10)]
    (println (str "Found " (.totalHits topdocs) " results."))
    (doseq [[i result] (indexed (get-documents reader (.scoreDocs topdocs)))]
      (println (str i " : " result)))
    (println "Took " (- (System/currentTimeMillis) start) " ms to search.")))
