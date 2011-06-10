(ns sandbox.lucene
  (:import (java.io File)
    (org.apache.lucene.analysis SimpleAnalyzer)
    (org.apache.lucene.document Document Field Field$Store Field$Index)
    (org.apache.lucene.index IndexReader IndexWriter IndexWriter$MaxFieldLength)
    (org.apache.lucene.queryParser QueryParser)
    (org.apache.lucene.search IndexSearcher)
    (org.apache.lucene.store SimpleFSDirectory)
    (org.apache.lucene.util Version)))

(defn create-analyzer []
  (SimpleAnalyzer.))

(defn create-index [path]
  (let [dir (-> (File. path) SimpleFSDirectory.)]
    (IndexWriter. dir (create-analyzer) IndexWriter$MaxFieldLength/UNLIMITED)))

(defn create-field [k v]
  (Field. (name k) (str v) Field$Store/YES Field$Index/ANALYZED))

(defn default-field-val [m]
  "Takes a map, returns the concatenation of all values."
  (apply str (interpose " " (vals m))))

(defn create-clj-document [data]
  (assoc data :_default (default-field-val data)))

(defn create-document [data]
  (let [doc     (Document.)
        default (create-clj-document data)]
    (do
      (doseq [[k v] default] (. doc add (create-field k v))) doc)))

(defn create-reader [path]
  (IndexReader/open (-> (File. path) SimpleFSDirectory.)))

(defn create-searcher [path]
  (IndexSearcher. (create-reader path)))

(defn create-query
  ([field q-string]
    (let [parser (QueryParser. Version/LUCENE_30 field (create-analyzer))]
      (. parser parse q-string)))
  ([q-string]
    (create-query "_default" q-string)))
