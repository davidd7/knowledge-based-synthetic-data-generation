from owlready2 import *

onto = get_ontology("file://ontologies/test1.owl")
onto.load()

# with onto is needed for test5 to be in class. Question is whether the old Bed is overwritten. Doesn't seem so because the storeid is same in both cases but that can also be implementation-specific
with onto:
    class Bed(Thing):
        test5 = 10
    class Bed(Thing):
        test10 = 15
    # Not expected: test5 and test10 are now both in Bed..!


    #Bed.
# class Bed(Thing):
#     test5 = 10

# onto_path.append("/ontologies/test1.owl")
# onto = get_ontology("http://www.semanticweb.org/david/ontologies/2022/6/untitled-ontology-4")

for el in onto.classes():
    print(el)
    print(el.__dict__)



class hello():
    test1 = 3
class hello():
    test2 = 5
hello.test3 = 10
print(hello.__dict__)
# test2 and test3 are both added, test1 is not there anymore



class hello10():
    pass
hello10.test3 = 10
class hello10():
    test2 = 5
print(hello10.__dict__)
# => test3 is not saved, as would be expected





# VERSUCH X1

# class BedTest(Thing.Lol):
#     test5 = 10
# -> Error: Lol is not defined


# with onto:
#     class BedTest(Thing.Lol):
#         test5 = 10
# -> Lol is not defined



# with onto:
#     class BedTest(Thing.Bed):
#         test5 = 10
# -> Bed is not defined


class BedTest(Bed):
    test5 = 10

# -> ist klar, dass die darüber nicht funktioniert haben. Macht ja keinen Sinn zu sagen Elternklasse.Kindklasse, ist ja Vererbung und nicht Attribut denke ich. Thing hat ja kein Bed, sondern Bed ist Form von Thing...



