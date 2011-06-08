(ns sandbox.db
  (:use [clojure.contrib.sql :only [with-connection]]))
(require ['clojureql.core :as 'cql])

(defn create-connection [path]
  {:classname   "org.sqlite.JDBC"
   :subprotocol "sqlite"
   :subname     path})

(defn results-of [conn ^String table]
  (with-connection conn
    (cql/with-results [rs (cql/table (keyword table))] (seq rs))))
    ;(cql/with-results [rs (cql/table (keyword table))]
    ;  (doseq [row rs]
    ;    (println row)))))

(defn enum-results []
  (let [conn  (create-connection "/home/rdrake/Downloads/uoit-mycampus.sq3")
        table "Courses"
        rs    (results-of conn table)]
    (doseq [row rs]
      (println row))))

(defn -main [& args]
  (enum-results))
