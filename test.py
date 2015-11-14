import mesh_structure.list_numpy as ln
import tree_view.meshDrawer as md
import time
from mesh_structure.MeshSlice import MeshSlice

# W katalogu mesh_tests znajdują się dwwa pliki do testów:
# duży_test.txt oraz test1.txt.
fileName = "mesh_tests/test1.txt"
# fileName = "mesh_tests/duzy_test.txt"

# Testowanie cięcia krawędzi. Ze względu na wersję testową działa tylko dla
# test1.txt (należy znać początkowy i końcowy wierzchołek, a dla tego testu
# są one wprowadzone w metodzie tnącej)
test_slice = False

# W przypadku pliku "duzy_test.txt" nie warto ustawiać depth_level na liczbę
# większą niż 10, ponieważ krawędzi jest wiele, czeka się długo, a wyniki nie
# wnoszą wiele więcej.
# Dla depth_level = 0 wyświetlają się wszystkie poziomy, jednak nie warto
# testować dla "duzy_test.txt"

depth_level = 4

start_time = int(round(time.time() * 100000))
mesh = ln.load_file(fileName)
mesh = ln.add_points(mesh)
mesh = ln.create_mesh_structure(mesh)

print ([ str(e) for e in mesh.contour])
    
end_time = int(round(time.time() * 100000))
print('czas: ' + str((end_time - start_time)/100000) + 's')

start_time = int(round(time.time() * 100000))
#mesh_slice = MeshSlice(mesh.contour)
#mesh_slice.depth_first_search()
print('czas: ' + str((end_time - start_time)/100000) + 's')

#if test_slice and fileName == "mesh_tests/test1.txt":
    #mesh_slice = MeshSlice(mesh.contour)
    #mesh_slice.depth_first_search()
    # md.draw_mesh_with_cutting_edge(mesh)
# else:
    # md.draw_mesh(mesh, depth_level)
