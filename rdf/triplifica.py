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
        L("OMAR is Ontology of the Art Museum of Rio",lang="en")
    )

G(      ns["omar"].data0+".rdf",
        ns["dcterms"].description,
        L("OMAR é a Ontologia do Museu de Arte do Rio",lang="pt")
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
for d in data:
    # forma a id com uri omar + id do pergamon OK
    wid=ID_GEN(ns["omar"].Artwork,d["pergamus_id"])
    # adiciona as outras ids, criando uma classe para cada uma delas
    if "Título Principal" in d.keys():
        G(  wid,
          ns["omar"].title,
          L(d["Título Principal"])
        )
    if "Assuntos" in d.keys():
        assuntos=d["Assuntos"].split(", ")
        for assunto in assuntos:
            G(  wid,
              ns["omar"].subject,
              L(assunto)
            )
    if "ISBN" in d.keys():
        isbn_=d["ISBN"]
        isbncount=isbn_.count("ISBN : ")
        if " / " in isbn_:
            isbn__,isbn1=isbn_.split(" / ")
            isbn2=isbn1.split("ISBN : ")[-1]
            idsbn=ID_GEN(ns["omar"].ID,isbn1)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn1)
            )
            idsbn=ID_GEN(ns["omar"].ID,isbn2)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn2)
            )
        elif isbncount==1:
            isbn1=isbn_.split(" : ")[-1]
            idsbn=ID_GEN(ns["omar"].ID,isbn1)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn1)
            )
        elif isbncount==2:
            isbn1,isbn2=isbn_.split("ISBN : ")[1:]
            idsbn=ID_GEN(ns["omar"].ID,isbn1)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn1)
            )
            idsbn=ID_GEN(ns["omar"].ID,isbn2)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn2)
            )
        elif isbncount==3:
            isbn1,isbn2,isbn3=isbn_.split("ISBN : ")[1:]
            idsbn=ID_GEN(ns["omar"].ID,isbn1)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn1)
            )
            idsbn=ID_GEN(ns["omar"].ID,isbn2)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn2)
            )
            idsbn=ID_GEN(ns["omar"].ID,isbn3)
            G(  wid,
              ns["omar"].id,
              idsbn
            )
            G(  idsbn,
              ns["omar"].value,
              L(isbn3)
            )


    # todas subclasse da classe ID

    # adiciona assuntos, títulos, edição

    # adiciona autor via classe entidade

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

# Fazer dicionário para as classes e propriedades relacionadas aos campos
# fazer só "obra" e linkar com os dados via propriedades?

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


