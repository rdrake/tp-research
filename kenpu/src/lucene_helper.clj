(ns lucene-helper
  (:import
    (java.io File)
    (org.apache.lucene.document Document Field Field$Store Field$Index)
    (org.apache.lucene.index IndexReader IndexWriter IndexWriter$MaxFieldLength)
    (org.apache.lucene.queryParser QueryParser)
    (org.apache.lucene.search IndexSearcher)
    (org.apache.lucene.store SimpleFSDirectory)
    (org.apache.lucene.util Version))
  (:use [clojure.contrib.str-utils]))

(println "Great. all ready to get started.")
(def version 0.1)

(defn make-analyzer 
  "Create a string analyzer"
  []
  (SimpleAnalyzer.))

(defn make-index-writer 
  "Create an index writer"
  [path]
  (let [dir (-> path File. SimpleFSDirectory.)]
    (IndexWriter. dir (make-analyzer) IndexWriter$MaxFieldLength/UNLIMITED)))

(defn make-document
  "Create a Lucene document"
  [& fields])
