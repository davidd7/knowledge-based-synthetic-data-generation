

import numpy as np
import trimesh

meshes = ["m1.stl", "m2.stl", "m1.stl", "m1.stl", "m2.stl", "m1.stl"]


print("\n####################################")
print("####### Here are the results #######")
print("####################################\n")

for mesh_path in meshes:
    mesh = trimesh.load(mesh_path)
    res = mesh.is_watertight
    print(f"• {mesh_path} { 'is' if res else 'is not' } watertight")


print("")


