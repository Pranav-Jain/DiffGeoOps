import numpy as np
from mayavi import mlab 
import pandas as pd
import sys


def read_off(file):
    if 'OFF' != file.readline().strip():
        raise('Not a valid OFF header')
    n_verts, n_faces, n_dontknow = tuple([int(s) for s in file.readline().strip().split(' ')])
    verts = [[float(s) for s in file.readline().strip().split(' ')] for i_vert in range(n_verts)]
    faces = [[int(s) for s in file.readline().strip().split(' ')][1:] for i_face in range(n_faces)]
    return verts, faces

def plot_curvatures(title, vertices, triangles, arr):
	mlab.figure(title)
	mesh = mlab.triangular_mesh(vertices[:,0], vertices[:,1], vertices[:,2], triangles, representation='wireframe', opacity=0) 
	mesh.mlab_source.dataset.point_data.scalars = arr
	mesh.mlab_source.dataset.point_data.scalars.name = 'Point data' 
	mesh.mlab_source.update() 
	mesh.parent.update()

	mesh2 = mlab.pipeline.set_active_attribute(mesh, 
	                point_scalars='Point data') 
	s2 = mlab.pipeline.surface(mesh2)
	s2.actor.mapper.interpolate_scalars_before_mapping = True
	mlab.colorbar(s2,title='Curvature', orientation='vertical')

	mlab.savefig(filename=title + '.png')
	mlab.show()

if __name__ == '__main__':

	if len(sys.argv) < 2:
			print("Input file missing")
			exit(0)

	elif len(sys.argv) == 2:
		f = open(sys.argv[1] ,'r')
		vertices, triangles = read_off(f)
		vertices = np.array(vertices)
		triangles = np.array(triangles)

	elif len(sys.argv) == 3:
		vertices = np.loadtxt(sys.argv[1], dtype=float)
		triangles = np.loadtxt(sys.argv[2], dtype=int) - 1

	else:
		print("Invalid Inputs")
		exit(0)


	df = pd.read_csv('output.csv')
	arr_K_H = np.array(df['Mean'])
	arr_K_G = np.array(df['Gaussian'])
	arr_K1 = np.array(df['Principal_1'])
	arr_K2 = np.array(df['Principal_2'])

	plot_curvatures('Mean', vertices, triangles, arr_K_H)
	plot_curvatures('Gaussian', vertices, triangles, arr_K_G)
	plot_curvatures('Principal_1', vertices, triangles, arr_K1)
	plot_curvatures('Principal_2', vertices, triangles, arr_K2)
