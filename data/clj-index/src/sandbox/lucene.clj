(ns sandbox.lucene
  (:import (java.io File)
           (org.apache.lucene.analysis SimpleAnalyzer)
           (org.apache.lucene.document Document Field Field$Store Field$Index)
           (org.apache.lucene.index IndexWriter IndexWriter$MaxFieldLength)
           (org.apache.lucene.queryParser QueryParser)
           (org.apache.lucene.search IndexSearcher)
           (org.apache.lucene.store SimpleFSDirectory)
           (org.apache.lucene.util Version)))

(defn create-analyzer []
  (SimpleAnalyzer.))

(defn create-index [path]
  (let [dir (-> (File. path) SimpleFSDirectory.)]
    (IndexWriter. dir create-analyzer IndexWriter$MaxFieldLength/UNLIMITED)))

(defn create-field [k v]
  (Field. k v Field$Store/YES Field$Index/ANALYZED))

(defn create-document [data]
  (let [doc (Document.)]
    (do
      (doseq [[k v] data] (. doc add (create-field k v))) doc)))

(defn create-searcher [path]
  (-> (File. path) SimpleFSDirectory. IndexSearcher.))

(defn create-query
  ([field q-string]
    (let [parser (QueryParser. Version/LUCENE_30 field create-analyzer)]
      (. parser parse q-string)))
  ([q-string]
    (create-query "_default" q-string)))
