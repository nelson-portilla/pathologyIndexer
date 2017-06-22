# -*- coding: utf-8 -*-
import os, sys
from flask import Flask, request, render_template
from IndexFiles import *
from SearchFiles import *

import sys, os, lucene, threading, time
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
global folder_path, folder_index

class Controller():
    
    global folder_path, folder_index


    def __init__(self):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        None

    @app.route('/')
    def cargar():
        global folder_path, folder_index
        #folder_path="/home/nelson/Documentos/leucene/data2"
        #folder_index="/home/nelson/Documentos/leucene/index"
        return render_template('index.html')
        print 'Carga del template OK'

    @app.route('/', methods=['POST'])
    def obtener():
        global folder_path, folder_index
        folder_path = str(request.form['folder_path'])
        folder_index = str(request.form['folder_index'])
        try:
            # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
            vm_env = lucene.getVMEnv()
            vm_env.attachCurrentThread()
            base_dir = os.path.dirname(os.path.abspath("folder_path"))
            count=IndexFiles().inicializar(folder_path, os.path.join(base_dir, folder_index),StandardAnalyzer())
            print count
        except Exception, e:
            print "Failed: ", e
            raise e
        #LLAMADO a la logica, index and search
        # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        # print 'lucene', lucene.VERSION
       

        # return render_template('index.html', objetos=["a", "b", "c"], texto="Texto Resultado", resultado="Total Resultados:")
        return render_template('index.html', cantidad="Se indexaron "+str(count)+" documentos! :)")

    @app.route('/search')
    def busqueda():
        return render_template('search.html')
        

    @app.route('/search', methods=['POST'])
    def buscar():
        global folder_path, folder_index
        # print folder_path
        # print folder_index
        palabra = str(request.form['id_entrada'])
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
        base_dir = os.path.dirname(os.path.abspath(folder_path))
        directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, folder_index)))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = StandardAnalyzer()
        SearchFiles().buscar(searcher, analyzer, palabra)
        listanombres=SearchFiles().getlistanombres()
        print "Lista controller: ",listanombres
        # print "Entro"
        return render_template('search.html', nombres=listanombres, resultado=str("Se encontraron "+str(len(listanombres))+" documentos!."))


if __name__=='__main__':
    # obj=Searching()
    # obj.get_doc()
    Controller()
    app.run(host='0.0.0.0', debug=True, port=8888, use_reloader=True)