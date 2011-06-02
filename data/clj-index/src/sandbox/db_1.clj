; KEN PU:
; sample code that performs multiple SQL queries and merges
; the results into a single "lazy" sequence
;

(ns sandbox.db-1
  (:use [clojure.contrib.sql :only [with-connection]]))
(require ['clojureql.core :as 'cql])

(def db {:classname   "org.sqlite.JDBC"
         :subprotocol "sqlite"
         :subname     "/home/kenpu/a.sq3"})

(defn results-of [table]
  (with-connection db
      (cql/with-results [rs (cql/table (keyword table))] (seq rs))))

(defn -main [& args]
  (print (results-of "T")))
