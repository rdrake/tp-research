(ns sandbox.db
  (:use [clojure.contrib.sql :only [with-connection]]))
(require ['clojureql.core :as 'cql])

(defn db [path]
  {:classname   "org.sqlite.JDBC"
   :subprotocol "sqlite"
   :subname     path})

(defn results-of [db ^String table]
  (with-connection db
    (cql/with-results [rs (cql/table (keyword table))] (seq rs))))

(defn -main [& args]
  (let [database (db "/home/rdrake/Downloads/uoit-mycampus.sq3")]
    (dorun (map #(println %) (results-of database "Courses")))))
