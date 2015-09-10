import mesh_structure.list_numpy as ln
import tree_view.meshDrawer as md
import time

# W katalogu mesh_tests znajdują się dwwa pliki do testów:
# duży_test.txt oraz test1.txt.
fileName = "mesh_tests/duzy_test.txt"
# fileName = "mesh_tests/test1.txt"

# Testowanie cięcia krawędzi. Ze względu na wersję testową działa tylko dla 
# test1.txt (należy znać początkowy i końcowy wierzchołek, a dla tego testu 
# są one wprowadzone w metodzie tnącej)
test_slice = True

# W przypadku pliku "duzy_test.txt" nie warto ustawiać depth_level na liczbę 
# większą niż 11, ponieważ krawędzi jest wiele, czeka się długo, a wyniki nie 
# wnoszą wiele więcej.
# Dla depth_level = 0 wyświetlają się wszystkie poziomy, jednak nie warto 
# testować dla "duzy_test.txt"

depth_level = 5

start_time = int(round(time.time() * 100000))
mesh = ln.load_file(fileName)
mesh = ln.add_points(mesh)
mesh = ln.create_mesh_structure(mesh)
end_time = int(round(time.time() * 100000))
print('czas: ' + str((end_time - start_time)/100000) + 's')

if test_slice and fileName == "mesh_tests/test1.txt":
    mesh.test()
    md.draw_mesh_with_cutting_edge(mesh)
else:
    md.draw_mesh(mesh, depth_level)


