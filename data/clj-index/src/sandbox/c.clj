; We are experimenting with Lucene in Clojure
;
(ns sandbox.c
  (:use clojure.contrib.str-utils)
  (:import (org.apache.lucene.document
             Document Field Field$Store Field$Index)
           (org.apache.lucene.analysis SimpleAnalyzer)
           (org.apache.lucene.store SimpleFSDirectory)
           (java.io File)
           (org.apache.lucene.search IndexSearcher)
           (org.apache.lucene.util Version)
           (org.apache.lucene.queryParser QueryParser)))

(def analyzer (SimpleAnalyzer.))

(defn create-searcher [path]
  (IndexSearcher. (SimpleFSDirectory. (File. path))))

(defn create-query [field q-string]
  (let [parser (QueryParser. Version/LUCENE_30 field analyzer)]
    (.parse parser q-string)))

(defn -main [path field q-string & args]
  (let [query (create-query field q-string)
        searcher (create-searcher path)
        topdocs (.search searcher query 10)]
    (println (str "We have found " (. topdocs totalHits)))))

