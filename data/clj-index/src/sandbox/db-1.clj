; KEN PU:
; sample code that performs multiple SQL queries and merges
; the results into a single "lazy" sequence
;

(ns sandbox.db-1
  (:use [clojure.contrib.sql :only [with-connection]]))
(require ['clojureql.core :as 'cql])

(def db {:classname   "org.sqlite.JDBC"
         :subprotocol "sqlite"
         :subname     "/home/rdrake/Downloads/uoit-mycampus.sq3"})

(defn -main [& args]
  (with-connection db
                  (cql/with-results [rs (cql/table :courses)]
                                    (doseq [r rs] (println (:title r))))))
