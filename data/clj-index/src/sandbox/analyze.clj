(ns sandbox.analyze
  (:import (org.apache.lucene.analysis SimpleAnalyzer)
           (org.apache.lucene.analysis Token)
           (org.apache.lucene.analysis.tokenattributes 
             OffsetAttribute TermAttribute)
           (java.io StringReader)))

(def *analyzer* (SimpleAnalyzer.))

(defn apply-analyzer 
  "returns a TokenStream"
  [analyzer field s]
  (.tokenStream analyzer field (StringReader. s)))

(declare token-stream-seq-2)

(defn token-stream-seq
  [stream]
  (let [offsetAttribute (.getAttribute stream OffsetAttribute)
        termAttribute (.getAttribute stream TermAttribute)]
    (token-stream-seq-2 stream offsetAttribute termAttribute [])))

(defn token-stream-seq-2
  [stream offsetAttribute termAttribute result]
  (do
    (let [more (.incrementToken stream)
          term (.term termAttribute)]
      (if more
        (recur stream offsetAttribute termAttribute (conj result term))
        result))))

(defn -main [& args]
  (let [s "HeLlO world what is up?"]
    (println (token-stream-seq (apply-analyzer *analyzer* "name" s)))))
