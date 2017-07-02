#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

import logging
from docs.config import *

from java.nio.file import Paths
from java.io import IOException
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.highlight import *

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

class SearchFiles(object):
    """docstring for SearchFiles"""
    
    global listanombres, listarutas
    listanombres=[]
    listarutas=[]

    def __init__(self):
        global listanombres, listarutas        
        print "SearchFiles Cargado"
        

    def buscar(self, searcher, analyzer, palabra): 
        global listanombres, listarutas   
        query = QueryParser("contents", analyzer).parse(palabra)
        scoreDocs = searcher.search(query, 50).scoreDocs
        listanombres=[]
        listarutas=[]

        #PARA HIGHLIGHT
        print "%s total matching documents." % len(scoreDocs)
        HighlightFormatter = SimpleHTMLFormatter();
        highlighter = Highlighter(HighlightFormatter, QueryScorer (query))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            
            ###
            text = doc.get("contents")
            ts = analyzer.tokenStream("contents", StringReader(text))
            print doc.get("path")
            #print highlighter.getBestFragments(ts, text, 3, "...")
            print ""
            ###

            # print 'path:', doc.get("path"), 'name:', doc.get("name")
            listanombres.append([doc.get("name"),doc.get("path"),highlighter.getBestFragments(ts, text, 3, "...")])



    def getlistanombres(self):
        global listanombres, listarutas
        return listanombres

    def getlistarutas(self):
        global listanombres, listarutas
        return listarutas

# if __name__ == '__main__':
#     lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    # print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    # directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    # searcher = IndexSearcher(DirectoryReader.open(directory))
    # analyzer = StandardAnalyzer()
    # run(searcher, analyzer)
    # del searcher
