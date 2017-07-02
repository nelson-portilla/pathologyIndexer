# -*- coding: utf-8 -*-
import os, sys
from flask import Flask, request, render_template
from IndexFiles import *
from SearchFiles import *

import logging
from docs.config import *

import sys, os, lucene, threading, time
from datetime import datetime
from java.io import StringReader
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
        logging.basicConfig(filename=LOG_FILE,\
            level=logging.INFO,\
            format='%(levelname)s[%(asctime)s]: %(message)s',\
            datefmt='%m/%d/%Y %I:%M:%S %p',filemode='a')
        logging.info("Archvo de log creado")

    @app.route('/')
    def cargar():
        global folder_path, folder_index
        #folder_path="/home/nelson/Documentos/pathologyIndexer/data"
        #folder_index="/home/nelson/Documentos/pathologyIndexer/index2"
        return render_template('index.html')
        logging.info("Cargando Template")

    @app.route('/', methods=['POST'])
    def indexar():
        global folder_path, folder_index
        #folder_path = str(request.form['folder_path'])
        #folder_index = str(request.form['folder_index'])
        try:
            # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
            logging.info("Obteniendo ambiente de lucene en indexar")
            vm_env = lucene.getVMEnv()
            logging.info("Creando hilo en el ambiente en indexar")
            vm_env.attachCurrentThread()
            #base_dir = os.path.dirname(os.path.abspath("folder_path"))
            logging.info("Llamando a IndexFiles.inicializar con: "+str(DATA_PATH)+","+str(INDEX_PATH)+",StandardAnalyzer")
            count=IndexFiles().inicializar(os.path.join(PUBLIC_PATH, DATA_PATH), INDEX_PATH, StandardAnalyzer())
            # count=IndexFiles().inicializar(folder_path, os.path.join(base_dir, folder_index),StandardAnalyzer())
            print count
        except Exception, e:
            logging.warning("Ha fallado en la indexacion")
            raise e
        #LLAMADO a la logica, index and search
        # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        # print 'lucene', lucene.VERSION
       

        # return render_template('index.html', objetos=["a", "b", "c"], texto="Texto Resultado", resultado="Total Resultados:")
        logging.info("Renderizando template en la indexacion")
        return render_template('index.html', cantidad="Se indexaron "+str(count)+" documentos! :)")

    @app.route('/search')
    def busqueda():
        logging.info("Ingresando en la vista principal de la busqueda")
        return render_template('search.html')
        

    @app.route('/search', methods=['POST'])
    def buscar():
        global folder_path, folder_index
        logging.info("Ingresando en la peticion para busqueda")
        # print folder_path
        # print folder_index
        logging.info("palabra buscada: "+request.form['id_entrada'])
        palabra = str(request.form['id_entrada'])
        logging.info("Obteniendo ambiente de lucene en busqueda")
        vm_env = lucene.getVMEnv()
        logging.info("Creando hilo en el ambiente en busqueda")
        vm_env.attachCurrentThread()
        #base_dir = os.path.dirname(os.path.abspath(folder_path))
        
        logging.info("Llamando a SimpleFSDirectory")
        directory = SimpleFSDirectory(Paths.get(INDEX_PATH))
        # directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, folder_index)))
        logging.info("Llamando a IndexSearcher")
        searcher = IndexSearcher(DirectoryReader.open(directory))
        logging.info("Llamando a StandardAnalyzer")
        analyzer = StandardAnalyzer()
        logging.info("Buscando palabra: "+palabra)
        SearchFiles().buscar(searcher, analyzer, palabra)
        listanombres=SearchFiles().getlistanombres()
        logging.info("Obteniendo la lista de nombres: "+str(listanombres))
        #print "Lista controller: ",listanombres
        # print "Entro"
        logging.info("Renderizando template de busqueda con resultado")
        return render_template('search.html', nombres=listanombres, resultado=str("Se encontraron "+str(len(listanombres))+" documentos!."))


if __name__=='__main__':
    # obj=Searching()
    # obj.get_doc()
    Controller()
    print "Aplicacion corriendo"
    print "http://localhost:8888"
    app.run(host='0.0.0.0', debug=True, port=8888, use_reloader=True)