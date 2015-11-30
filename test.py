import mesh_structure.list_numpy as ln
import time
import tree_view.meshDrawer as md

fileName = "mesh_tests/test2.txt"


def create_mesh(fileName=fileName):
    mesh = ln.load_file(fileName)
    mesh = ln.add_points(mesh)
    return ln.create_mesh_structure(mesh)

start_time = int(round(time.time() * 100000))
# print([str(v) for v in mesh.contour.contour])
# mesh.contour.slice_contour()

#ln.test_slice(mesh)

mesh = create_mesh(fileName)
#print([str(e) for e in mesh.contour.contour])
#print(mesh.vertex_list.vertex_tree)

end_time = int(round(time.time() * 100000))
print('czas: ' + str((end_time - start_time)/100000) + 's')

#md.draw_mesh_with_cutting_edge(mesh)
#md.draw_mesh(mesh, 7)
