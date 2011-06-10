(ns sandbox.db
  (:use [clojure.contrib.sql :only [with-connection]])
  (:use [sandbox.lucene :only [create-document create-index]]))
(require ['clojureql.core :as 'cql])

(defn create-connection [path]
  {:classname   "org.sqlite.JDBC"
   :subprotocol "sqlite"
   :subname     path})

(defn results-of [conn ^String table fcn]
  (with-connection conn
    (cql/with-results [rs (cql/table (keyword table))]
      (doseq [row rs]
        (fcn row)))))
