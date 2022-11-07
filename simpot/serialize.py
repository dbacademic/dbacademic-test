from rdflib import Graph

import types

## serialize

def mapper_item (data, value):
    if isinstance(value, types.FunctionType):
        return value (data)
    if isinstance(value, str):
        return data[value]

def mapper_one (mapper, data ):
    return {item : mapper_item (data, value) for (item, value) in mapper.items()} 

def mapper_all (mapper, data):
    return map (lambda d: mapper_one(mapper, d), data  )

def serialize_to_rdf (data, type_class ):
    rdf = list( map(lambda d: type_class (d), data ) )
    return (graph(rdf)).serialize() #.decode()

def serialize_to_rdf_file (data, type_class, path ):
    f = open(path,"w+",encoding="utf-8") 
    print ("saving ..."+path)
    f.write (serialize_to_rdf(data, type_class))
    f.close()

def serialize_all_to_rdf (data):
    for tordf in data["collection"]:
        if tordf["toSave"]:
            serialize_to_rdf_file ( mapper_all( tordf["mapper"], tordf["data"]()) , data["classType"], tordf["rdf_path"] )


def graph (value):
    if isinstance(value, list):
        gtotal = Graph()
        for o in value:
            for n in o.g.namespaces():
                gtotal.bind(n[0], n[1])
            for s, p, o in o.g:
                gtotal.add ((s,p,o))

        return gtotal
    else:
        return value.g