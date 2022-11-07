from rdflib import Namespace, Literal, URIRef,RDF
from simpot import RdfsClass, BNamespace, graph
from rdflib.namespace import DC, FOAF

import hashlib

from simpot import serialize_to_rdf

import requests




## utils
def hashcode (university, resource,  code):
  return hashlib.md5((university+resource+code).encode()).hexdigest()

def dados_ckan (url):
    data = requests.get(url+"&limit=30").json()
    print (len (data["result"]["records"] ))
    return data["result"]["records"]



## modelo
DC = Namespace('http://purl.org/dc/terms/#')
ORG = Namespace ("https://www.w3.org/TR/vocab-org/")
OPENCIN = Namespace("http://purl.org/ontology/opencin/")


UFRN="http://dbpedia.org/resource/Federal_University_of_Rio_Grande_do_Norte"


class Discente ():

    nome = FOAF.name
    curso = OPENCIN.isMemberOf
    code= DC.identifier

    university = ORG.memberOf

    @RdfsClass(OPENCIN.Student, "https://www.dbacademic.tech/resource/")
    @BNamespace('foaf', FOAF)
    @BNamespace('cin', OPENCIN)
    @BNamespace('dc', DC)
    def __init__(self, dict ): ## um desafio é que cada instituição, os atributos estarão diferentes
        self.nome = Literal(dict["nome_discente"])
        self.id = hashcode ("ufrn", "discente", dict["matricula"])
        self.code = dict["matricula"]
        if "id_curso" in dict:
            self.curso = URIRef("https://www.dbacademic.tech/resource/" +  hashcode ( "ufrn", "curso", str (dict["id_curso"])))
        self.university = URIRef(UFRN)



## extraindo
dados = dados_ckan("http://dados.ufrn.br/api/action/datastore_search?resource_id=a55aef81-e094-4267-8643-f283524e3dd7")

## convertendo
print (serialize_to_rdf(dados, Discente))

