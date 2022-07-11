

# Declare functions, which will normally be in another file probably
import blenderproc as bproc


def CreateArea(
    x=None,
    y=None,
    z=None,
    x_length=None,
    y_length=None,
    z_length=None,
    keys=[]):
    pass
    test = bproc.object.create_primitive(shape="CUBE")
    test.set_scale( [x_length/2,y_length/2,z_length/2] ) # Cube ist standardmäßig 2m x 2m x 2m groß. Scale von 10 in einer Richtung führt also zu 20m Länge in dieser Richtung
    test.set_location( [  x + x_length/2  ,  y + y_length/2  ,  z + z_length/2  ] ) # location bezieht auf Mittelpunkt des Objektes. Das ist für Modelle ggf. oft cool, für Rechteck wär aber auch cool genau ausmessen zu können, weswegen anpassen werde
    



def CreateCamera():
    pass


def CreateObjects(objects=[], how_many=None, keys=None):
    pass

def AddIterationTasks(list_of_tasks = []):
    pass

def RandomVisibleObjects(key=None, min=None, max=None):
    pass

def StartGeneration():
    pass















def CreateUniqueKey():
    i = 0
    while True:
        i += 1
        yield f"unique_key_{i}"



# 01 - Initialize parameters as one would get them as inputs to algorithm-side

params = {
    "objects": [
        {
            "model" : "models/dragon.obj",
            "quantity" : {
                "min" : 5,
                "max" : 5
            }
        },
        {
            "model" : "models/nut2.obj",
            "quantity" : {
                "min" : 5,
                "max" : 5
            }
        }
    ],
    "area": {
        "length_in_x" : 3,
        "length_in_y" : 3
    },
    "camera" : {
        "height" : 10
    }
}



print(params)



# 03 - Combining the parameters and functions to generate synthetic data

CreateArea(
    x = - params["area"]["length_in_x"] / 2,
    y = - params["area"]["length_in_y"] / 2,
    z = 20,
    x_length = params["area"]["length_in_x"],
    y_length = params["area"]["length_in_y"],
    z_length = 0,
    keys = ["area_objects"]
)

CreateArea(
    x = - params["area"]["length_in_x"] / 2,
    y = - params["area"]["length_in_y"] / 2,
    z = params["camera"]["height"],
    x_length = params["area"]["length_in_x"],
    y_length = params["area"]["length_in_y"],
    z_length = 0,
    keys = ["area_cameras"]
)



CreateCamera()


for el in params["objects"]:
    uniq = CreateUniqueKey()
    CreateObjects(objects=[el], how_many=el["quantity"]["max"], keys=["to_recognize", uniq])
    AddIterationTasks(
        RandomVisibleObjects(key=uniq, min=el["quantity"]["min"], max=el["quantity"]["max"])
    )


StartGeneration()

























































































































