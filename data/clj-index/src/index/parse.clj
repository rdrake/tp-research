(ns index
  (:require [clojure.xml :as xml]
            [clojure.zip :as zip]
            [clojure.contrib.zip-filter.xml :as zf]))

(defn get-ids [zipper]
  (zf/xml -> zipper :title zf/text))

(println (get-ids
           (zip/xml-zip
             (xml/parse "/home/rdrake/Downloads/dblp.xml"))))
