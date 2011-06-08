(ns index.index.lucene
  ;(:use [index.index.index :only [Index]])
  (:require [index.index :as index])
  (:import (index.index Index))
  (:import (java.io File)
           (org.apache.lucene.analysis SimpleAnalyzer)
           (org.apache.lucene.document Document Field Field$Store Field$Index)
           (org.apache.lucene.index IndexWriter IndexWriter$MaxFieldLength)
           (org.apache.lucene.queryParser QueryParser)
           (org.apache.lucene.search IndexSearcher)
           (org.apache.lucene.store SimpleFSDirectory)
           (org.apache.lucene.util Version)))

(deftype Lucene [path analyzer]
  Index
  (create-index [path]
                (let [dir (-> (File. path) SimpleFSDirectory.)]
                  (IndexWriter. dir analyzer IndexWriter$MaxFieldLength/UNLIMITED)))

  (create-field [k v]
                (Field. k v Field$Store/YES Field$Index/ANALYZED))

  (create-document [data]
  (let [doc (Document.)]
    (do
      (doseq [[k v] data] (. doc add (create-field k v)))
      doc)))

  (create-searcher [path]
                   (-> (File. path) SimpleFSDirectory. IndexSearcher.))

  (create-query [field q-string]
                (let [parser (QueryParser. Version/LUCENE_30 field analyzer)]
                  (. parser parse q-string))))

(defn -main [& args]
  (println "Lucene!"))
