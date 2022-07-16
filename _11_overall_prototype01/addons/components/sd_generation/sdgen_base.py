from owlready2 import *

#path = "C:\Users\david\Git Repositories\MATSE-bachelorarbeit-ss22-tests\_10_ontologie_tests\ontologies"
path = "C:/Users/david/Git Repositories/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies"
onto = get_ontology(f"file://{path}/sdgen_ontology_1.owl") # get_ontology("file://../../data/ontologies/sdgen_ontology_1.owl")
onto.load()




with onto:
    pass



#for el in onto.classes():
    #print(el)
    #print(el.__dict__)


test = onto.EGS1
print(test)


# res = list(default_world.sparql(""" SELECT (COUNT(?x) AS ?nb) { ?x a owl:Class . } """))
# res = list(default_world.sparql(""" SELECT (COUNT(?x) AS ?nb) { ?x rdfs:label "GenerationScheme" . } """))
# res = list(default_world.sparql(""" SELECT (COUNT(?x) AS ?nb) { ?x rdfs:subClassOf* "GenerationScheme" . } """))

#res = list(default_world.sparql(""" SELECT ?x { ?x rdfs:subClassOf* "GenerationScheme" . } """))
#res = list(default_world.sparql(""" SELECT ((?x) AS ?nbc) { ?x rdfs:subClassOf* "GenerationScheme" . } """))

res = list(default_world.sparql("""
           SELECT ?y
           { ?y a "GenerationScheme" .}
    """))

# res = list(default_world.sparql("""
#            SELECT ?y
#            { ?y a owl:Class }
#     """))


res = list(default_world.sparql("""
           SELECT ?y
           { ?x rdfs:label "GenerationScheme" .
             ?y a/rdfs:subClassOf* ?x }
    """))




# res = list(default_world.sparql("""
#            SELECT ?y
#            { ?x rdf:about "http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation#GenerationScheme" .
#              ?y a/rdfs:subClassOf* ?x }
#     """))
# -> geht noch nicht. bislang ist einzige Option die ich sehe überall label hinzufügen (oder weiter suchen, wie mit Namen finden kann)


res = onto.search(type=onto.GenerationScheme)


print(res)

for el in res:
    print("lol")
    print(el.__dict__)
    pass

print(res[0].Has_Volume)











