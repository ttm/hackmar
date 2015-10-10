import json
from pprint import pprint as pp
import rdflib as r
import percolation as pe

with open('../acervo.json') as data_file:    
    data = json.load(data_file)

#pp(data)

###########
### Namespaces usados na triplificação
#rdf = r.namespace.RDF
#foaf = r.namespace.FOAF
#xsd = r.namespace.XSD
#mar = r.Namespace("http://purl.org/socialparticipation/mar/")

g = r.Graph()
#g.namespace_manager.bind("rdf", r.namespace.RDF)    
#g.namespace_manager.bind("foaf", r.namespace.FOAF)    
#g.namespace_manager.bind("xsd", r.namespace.XSD)    
#g.namespace_manager.bind("mar", "http://purl.org/socialparticipation/mar/")

def G(S,P,O):
    g.add((S,P,O))
def L(data, datatype=None,lang=None):
    if datatype and lang:
        return r.Literal(data, datatype=datatype,lang=lang)
    elif datatype:
        return r.Literal(data, datatype=datatype)
    elif lang:
        return r.Literal(data, lang=lang)
    else:
        return r.Literal(data)

def namespaces(ids=[]):
    """Declare namespace URIs in RDF graph and return a dictionary of them.
    
    input: list of ids. Use tuple for (idstring, URIString) of
    benefint from RDFLib and particpatory IDs 
    throughtput: declare RDF in graph g
    output: dictionary of {key=id, value=URI} as declared
    
    Deals automaticaly with namespaces from RDFlib and selected
    participatory libs"""
    idict={}
    for tid in ids:
        # findig URIRef 
        if type(tid)!=type("fooString"): # tuple (tid,iuri)
            idict[tid[0]]=r.Namespace(tid[1])
        elif tid in [fooString.lower() for fooString in dir(r.namespace)]: # rdflib shortcut
            if tid in dir(r.namespace):
                idict[tid]=eval("r.namespace."+tid)
            else:
                idict[tid]=eval("r.namespace."+tid.upper())
        else: # participatory shortcut
            idict[tid]=r.Namespace("http://purl.org/socialparticipation/{}/".format(tid))
        # adding to RDF Graph
        if type(tid)!=type("fooString"): # tuple (tid,iuri)
            g.namespace_manager.bind(tid[0], idict[tid[0]])    
        else:
            g.namespace_manager.bind(tid, idict[tid])    
    return idict

def ID_GEN(namespace,tid):
    ind=namespace+"#"+tid
    G(ind,ns["rdf"].type,namespace)
    return ind




ns=namespaces=namespaces(["rdf","rdfs","owl","xsd", # basic namespaces
                          "omar", # participatory namespaces
                          "dcterms","dc", # useful Dublincore Metadata
                          ])

# Info about ORe
#g.add((ouri,dct.description,r.Literal(u"Ontologia do Participa.br, levantada com base nos dados e para conectar com outras instâncias")))
G(      ns["omar"].data0+".rdf",
        ns["dcterms"].description,
        L("OMAR is Ontology of the Art Museum of Rio de Janeiro",lang="en")
    )

G(      ns["omar"].data0+".rdf",
        ns["dcterms"].description,
        L("OMAR é a Ontologia do Museu de Arte Rio",lang="pt")
    )
isbn=[]
keys=[]
ta=[]
for d in data:
    keys+=list(d.keys())
keys_=set(keys)
tdict={}
for key in keys_:
    tdict[key]=[]
for d in data:
    keys__=list(d.keys())
    for key in keys__:
        tdict[key]+=[d[key]]
#    if "ISBN" in d.keys():
#        isbn.append(d["ISisbnisbnBN"]+"\n")
#    if "Título do Artigo" in d.keys():
#        ta.append(d["Título do Artigo"]+"\n")
for key in keys_:
    f=open("txt/"+key.replace("/","").replace(" ","")+".txt","w")
    f.writelines([i+"\n" for i in tdict[key]])
    print(len(tdict[key]), key)
    f.close()
#f=open("ta.txt","w")
#f.writelines(ta)
#f.close()


# análise mínima dos dados
print(len(keys_), "campos", keys_)
#print(len(tdict["ISBN"]), "ISBNs")
#print(len(tdict["Título do Artigo"]), "títulos de artigos")
#print(len(tdict["Número de Chamada"]), "números de chamada")
#print(len(tdict['Outros Títulos']), "outros títulos")
#print(len(tdict['Autor do Artigo']), 'Autor do Artigo')
#print(len(tdict['Título Principal']), 'Título Principal')
#print(len(tdict['Título Posterior']), 'Título Posterior')
#print(tdict['Título Posterior'], 'Título Posterior')
#print(len(tdict['Notas']), 'Notas')
print("Catalogação Pré MARC", "Só tem barra n!!!!")


