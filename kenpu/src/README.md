(ns lucene-helper)

  Code for maintaining the text index.

  - functions to create on-disk indexes
  - functions for building lucene documents
    (create-document 
      [:field name :value str :store :analyze :index]
      [:field name :value str :store :analyze :index]
      [:field name :value str :store :analyze :index])
  - functions for building lucene queries
  - functions for querying on-disk indexes to retrieve lucene documents
  - functions for mapping lucene documents to clojure maps

