from rdflib import Namespace, Literal, URIRef,RDF
from simpot import RdfsClass, BNamespace, graph
from rdflib.namespace import DC, FOAF

import hashlib

from simpot import serialize_to_rdf

import requests

import types

UFRN="http://dbpedia.org/resource/Federal_University_of_Rio_Grande_do_Norte"




## utils
def hashcode (university, resource,  code):
  return hashlib.md5((university+resource+code).encode()).hexdigest()

def dados_ckan (url):
    data = requests.get(url+"&limit=100").json()
    print (len (data["result"]["records"] ))
    return data["result"]["records"]


def mapper_item (data, value):
    if isinstance(value, types.FunctionType):
        return value (data)
    if isinstance(value, str):
        return data[value]

def mapper_one (mapper, data ):
    return {item : mapper_item (data, value) for (item, value) in mapper.items()} 

def mapper_all (mapper, data):
    return list(map (lambda d: mapper_one(mapper, d), data  ))


     
mapper = {
                    "nome" : "nome_discente", 
                    "id": lambda d: hashcode ("ufrn", "discente", d["matricula"]),
                    "code" : "matricula",
                    "university" : lambda d: UFRN,
                    "curso": lambda d: "https://www.dbacademic.tech/resource/" +  hashcode ( "ufrn", "curso", str (d["id_curso"]))
}


## extraindo
dados = dados_ckan("http://dados.ufrn.br/api/action/datastore_search?resource_id=a55aef81-e094-4267-8643-f283524e3dd7")
#dado1 = dados[0] 
#dado2 = mapper_one(mapper, dado1)
print (list(mapper_all(mapper, dados)))