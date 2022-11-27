

from rdflib import Namespace, Literal, URIRef,RDF
from simpot import RdfsClass, BNamespace, graph
from rdflib.namespace import DC, FOAF

from rdflib import Graph

class Person:
    nick = FOAF['nick']
    #name = FOAF.name
    #email = FOAF.mbox

    @RdfsClass(FOAF.Person, "http://example.com/") # blank node
    @BNamespace("dc", DC)
    @BNamespace("foaf", FOAF)
    def __init__ (self, name, nick, email):
        self.id = nick
        self.nick = Literal(nick, lang="foo")
        self.name = Literal (name)
        self.email = URIRef(email) 


#Person.name = FOAF.name
setattr(Person,"name", FOAF["name"])
Person.email = FOAF.mbox


p = Person ("Donna Fales","donna", "mailto:donna@example.org")
#print (graph(p).serialize())


def f():
    namespace = "http://www.opengis.net/ont/geosparql#"
    g = Graph()
    #g.parse(namespace, format="turtle")
    g.parse(namespace, format="xml")
    q = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?p
        WHERE {
            ?p rdf:type owl:DatatypeProperty.
            ?p rdf:type owl:ObjectProperty.
        }
    """

    # Apply the query to the graph and iterate through results

    for r in g.query(q):
        attr = r["p"].split("#") 
        print(attr)

namespaces = {
    'cell':  (Namespace("http://purl.org/ontology/dbcells/cells#"), 'turtle'),
    #'geo' : (Namespace ("http://www.opengis.net/ont/geosparql#"), 'xml'),
}

class Teste:

    def __init__(self):
        pass

    def loadVocabulary(self, namespace, fformat):
        #namespace = "http://purl.org/ontology/dbcells/cells#"
        g = Graph()
        g.parse(namespace, format=fformat)
        q = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            SELECT ?p
            WHERE 
            {
               { ?p rdf:type owl:DatatypeProperty} UNION
               { ?p rdf:type owl:ObjectProperty}
            }
        """

        # Apply the query to the graph and iterate through results
        vs = []
        for r in g.query(q):
            attr = r["p"].split("#") 
            vs.append(attr)
        return vs

    def loadVocabularies(self):
        self.vocabularies = []
        for (namespace, format) in namespaces.values():
            print (namespace, format)
            self.vocabularies = self.vocabularies + self.loadVocabulary(namespace, format)

CELL = Namespace("http://purl.org/ontology/dbcells/cells#")
GEO = Namespace ("http://www.opengis.net/ont/geosparql#")

class Cell ():
    
    asWkt = GEO.asWKT
    resolution = CELL.resolution
    
    @RdfsClass(CELL.Cell,"http://www.dbcells.org/epsg4326/")
    @BNamespace('geo', GEO)
    @BNamespace('cells', CELL)
    def __init__(self, dict):
        self.id = dict["id"]
        self.asWkt = Literal(dict["asWkt"])
        self.resolution = Literal(dict["res"])

QB = Namespace ("http://purl.org/linked-data/cube/")
AMZ = Namespace ("http://purl.org/ontology/dbcells/amazon")

class Observation ():
    
    
    refCell = CELL.refCell
    forest = AMZ.Percentage_of_Forest
    
    @RdfsClass(QB.Observation,"http://www.dbcells.org/amazon/observations/")
    @BNamespace('qb', QB)
    @BNamespace('amz', AMZ)
    def __init__(self, dict):
        self.id = dict["id"]
        self.refCell = URIRef(dict["refCell"])
        self.forest = Literal(dict["forest"])
    


celulas = [{"id": "1", "asWkt" : "Point 2 4", "res": 1}]
obs = [{"id": "2", "refCell": "http://www.dbcells.org/epsg4326/1", "forest": 0.67}] 

cs1 = list (map (lambda d: Cell (d), celulas))
cs2 = list (map (lambda d: Observation (d), obs))


#g1 = graph (cs1)
#g2 = graph (cs2)

#g3 = g1 + g2

#print (g2.serialize())

t = Teste()
t.loadVocabularies()
print (t.vocabularies)