; We are experimenting with Lucene in Clojure
;
(ns sandbox.b
  (:use clojure.contrib.str-utils)
  (:import (org.apache.lucene.document
             Document Field Field$Store Field$Index)
           (org.apache.lucene.analysis SimpleAnalyzer)
           (org.apache.lucene.store SimpleFSDirectory)
           (java.io File)
           (org.apache.lucene.index IndexWriter IndexWriter$MaxFieldLength)))

; 1. Create the index
(def analyzer (SimpleAnalyzer.))

(defn create-index [path]
  (let [dir (SimpleFSDirectory. (File. path))]
    (IndexWriter. dir analyzer IndexWriter$MaxFieldLength/UNLIMITED)))

; 2. Create some documents

(defn #^Field create-field [k v]
  (Field. k v Field$Store/YES Field$Index/ANALYZED))

(defn create-document [data]
  (let [#^Document doc (Document.)]
    (do
      (doseq [[k v] data] (. doc add (create-field k v)))
      doc)))

(defn -main [& args]
  (println "Hello world")
  (let [index (create-index "./myindex")
        doc1 (create-document {"name" "Ken Pu" "address" "101 Bloor Street East"})
        doc2 (create-document {"name" "Richard Drake" 
                               "address" "2000 Simcoe Street North"})]
    (doto index 
      (.addDocument doc1)
      (.addDocument doc2)
      .commit
      .close)))

