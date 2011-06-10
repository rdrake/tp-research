(ns sandbox.index
  (:use [sandbox.db :only [results-of create-connection]])
  (:use [sandbox.lucene :only [create-document create-index]]))

(defn index-table [conn index table]
  (results-of conn table (fn [m] (. index addDocument (create-document m)))))

(defn -main [db-path index-path & args]
  (let [conn    (create-connection db-path)
        index   (create-index index-path)
        tables  ["Courses" "Instructors" "Schedules" "Sections" "Teaches"]]
    (doseq [table tables] (index-table conn index table))
    (doto index
      .commit
      .close)))
