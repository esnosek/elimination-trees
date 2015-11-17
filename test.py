import mesh_structure.list_numpy as ln
import time

fileName = "mesh_tests/test1.txt"

start_time = int(round(time.time() * 100000))

mesh = ln.load_file(fileName)
mesh = ln.add_points(mesh)
mesh = ln.create_mesh_structure(mesh)

# print([str(v) for v in mesh.contour.contour])
# mesh.contour.slice_contour()

ln.test_slice()

end_time = int(round(time.time() * 100000))
print('czas: ' + str((end_time - start_time)/100000) + 's')

# md.draw_mesh_with_cutting_edge(mesh)
# md.draw_mesh(mesh, depth_level)
