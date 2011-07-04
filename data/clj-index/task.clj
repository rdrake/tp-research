(deftask start
  (invoke run {:run (:start cake/*opts*)}))

(defile index "uoit.idx" #{"uoit-mycampus.sq3"}
  "This task generates the UOIT index."
  (load-file "src/index/lucene/index.clj")
  (index.lucene.index/-main "uoit-mycampus.sq3" "uoit.idx"))
