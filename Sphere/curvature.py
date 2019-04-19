import numpy as np
import itertools

def read_off(file):
    if 'OFF' != file.readline().strip():
        raise('Not a valid OFF header')
    n_verts, n_faces, n_dontknow = tuple([int(s) for s in file.readline().strip().split(' ')])
    verts = [[float(s) for s in file.readline().strip().split(' ')] for i_vert in range(n_verts)]
    faces = [[int(s) for s in file.readline().strip().split(' ')][1:] for i_face in range(n_faces)]
    return verts, faces

def get_area(a,b,c): # area of triangle using heron's formula
	v1 = get_vector(a,b)
	v2 = get_vector(a,c)
	v3 = get_vector(b,c)
	
	x = np.linalg.norm(v1)
	y = np.linalg.norm(v2)
	z = np.linalg.norm(v3)
	s = (x+y+z)/2.0

	area = (s*(s-x)*(s-y)*(s-z))**0.5
	return area

def check_obtuse(triangle,vertices,index): # checks if triangle is obtuse
	flag=0

	x = vertices[index]
	ind_arr = []
	ind_arr.append(index)
	arr = different_elements(triangle,ind_arr)
	y = vertices[int(arr[0])]
	z = vertices[int(arr[1])]

	v1 = get_vector(x,y)
	v2 = get_vector(x,z)
	tan = get_tan_angle(v1,v2)
	if tan<0:
		flag=1
	v1 = get_vector(y,z)
	v2 = get_vector(y,x)
	tan = get_tan_angle(v1,v2)
	if tan<0:
		flag=2
	v1 = get_vector(z,x)
	v2 = get_vector(z,y)
	tan = get_tan_angle(v1,v2)
	if tan<0:
		flag=2

	return flag

def get_vector(x,y): # returns vector from x to y
	return y-x

def get_tan_angle(x,y): # return tan of angle between vectors x and y
	cos = np.dot(x.T,y)/(np.linalg.norm(x,2)*np.linalg.norm(y,2))
	tan = ((1-cos*cos)**0.5/(cos))
	# if tan<0:
	# 	# print('obtuse')
	# 	return(-1)
	return tan

def get_neighbors(index,triangles): # get 1 ring neighborhood for ith vertex
	ring_neighbors = []
	for tri in triangles:
		if index in tri:
			ring_neighbors.append(tri)

	# print(ring_neighbors)

	neighbors_in_order = get_common_edges(index,ring_neighbors)
	return np.array(neighbors_in_order)

def common_elements(list1, list2): # get common elements of list1 and list2
	return list(set(list1) & set(list2))

def different_elements(list1, list2): # get uncommon elements of list1 and list2
	return list(set(list1) ^ set(list2))

def get_common_edges(index,neighbors): #get triangles with common edges

	permutations = itertools.permutations(neighbors,len(neighbors))

	for matrix in permutations:
		flag = 0
		for i in range(len(matrix)):
			common = common_elements(matrix[i],matrix[(i+1)%len(matrix)])

			if len(common)!=2:
				flag=1
				break

		if flag==0:
			M = np.array(matrix)
			return(M)

def A_mixed(i,vertex,vertices,triangles):

	# print(vertex)
	A_mixed = 0
	neighbors = get_neighbors(i,triangles)
	# print('jkbckja',neighbors)
	# print(neighbors.type())
	if neighbors.dtype==object:
		return '#'

	summation = 0
	for j in range(neighbors.shape[0]):
		triangle1 = neighbors[j]
		triangle2 = neighbors[(j+1)%neighbors.shape[0]]

		flag1 = check_obtuse(triangle1,vertices,i)
		flag2 = check_obtuse(triangle2,vertices,i)

		# print(flag1)

		if flag1==0: # not obtuse
		
			common_vertices = common_elements(triangle1, triangle2)
			arr = np.delete(common_vertices,np.where(common_vertices==np.float64(i)))
			# print(arr)
			
			x1 = vertex
			x2 = vertices[int(arr[0])]

			a = vertices[int(different_elements(triangle1, common_vertices)[0])]
			b = vertices[int(different_elements(triangle2, common_vertices)[0])]

			v1 = get_vector(a,x1)
			v2 = get_vector(a,x2)
			cot_alpha = 1.0/get_tan_angle(v1,v2)

			v1 = get_vector(b,x1)
			v2 = get_vector(b,x2)
			cot_beta = 1.0/get_tan_angle(v1,v2)

			summation += ((cot_alpha + cot_beta) * (np.linalg.norm(x1-x2)**2))/8.0

		elif flag1==1:
			area = get_area(vertices[triangle1[0]],vertices[triangle1[1]],vertices[triangle1[2]])
			summation += area/2.0
		else:
			area = get_area(vertices[triangle1[0]],vertices[triangle1[1]],vertices[triangle1[2]])
			summation += area/4.0

	A_mixed += summation

	print('A_mixed', A_mixed)
	return A_mixed

def mean_normal_curvature(i,vertex,A_mixed,vertices,triangles):
	neighbors = get_neighbors(i,triangles)
	summation = np.array([0.,0.,0.])

	for j in range(neighbors.shape[0]):
		triangle1 = neighbors[j]
		triangle2 = neighbors[(j+1)%neighbors.shape[0]]
		
		common_vertices = common_elements(triangle1, triangle2)
		arr = np.delete(common_vertices,np.where(common_vertices==np.float64(i)))
		
		x1 = vertex
		x2 = vertices[int(arr[0])]

		a = vertices[int(different_elements(triangle1, common_vertices)[0])]
		b = vertices[int(different_elements(triangle2, common_vertices)[0])]

		v1 = get_vector(a,x1)
		v2 = get_vector(a,x2)
		cot_alpha = 1.0/get_tan_angle(v1,v2)

		v1 = get_vector(b,x1)
		v2 = get_vector(b,x2)
		cot_beta = 1.0/get_tan_angle(v1,v2)

		summation += (cot_alpha + cot_beta) * (x1-x2)

	K = summation/(2.0*A_mixed)
	return K

def gaussian_curvature(i,vertex,A_mixed,vertices,triangles):
	neighbors = get_neighbors(i,triangles)

	summation = 0.
	for j in range(neighbors.shape[0]):
		triangle = neighbors[j]
		arr = np.delete(triangle,np.where(triangle==i))

		a = vertices[int(arr[0])]
		b = vertices[int(arr[1])]
		c = vertices[int(i)]

		v1 = get_vector(c,a)
		v2 = get_vector(c,b)
		theta = np.arctan(get_tan_angle(v1,v2))

		# print(theta)
		summation += theta

	K_G = (2.*np.pi - summation)/(A_mixed)
	return K_G

def mean_curvature(K):
	K_H = np.linalg.norm(K,2)/2.
	return K_H

def principal_curvature(K_H,K_G):
	delta = K_H*K_H - K_G
	# print(delta)
	if delta<0:
		delta=0

	K1 = K_H + delta**0.5
	K2 = K_H - delta**0.5

	return K1,K2

if __name__ == '__main__':

	vertices = np.loadtxt("2wcV.txt", dtype=float)
	triangles = np.loadtxt("2wcT.txt", dtype=int)-1

	# f = open('./Cylindroid/cylindroid.off','r')
	# vertices, triangles = read_off(f)
	# vertices = np.array(vertices)
	# triangles = np.array(triangles)
	# print(vertices.shape)

	arr_K_H = np.zeros(triangles.shape[0])
	arr_K_G = np.zeros(triangles.shape[0])
	arr_K1 = np.zeros(triangles.shape[0])
	arr_K2 = np.zeros(triangles.shape[0])
	
	for i in range(len(vertices)):
		print('\nVertex: ' + str(i))

		a_mixed = A_mixed(i,vertices[i],vertices,triangles)
		if a_mixed=='#' or a_mixed==0:
			print('#')
			continue

		K = mean_normal_curvature(i,vertices[i],a_mixed,vertices,triangles)
		K_H = mean_curvature(K)
		K_G = gaussian_curvature(i,vertices[i],a_mixed,vertices,triangles)

		K1, K2 = principal_curvature(K_H,K_G)

		print('K',K)
		print('K_H',K_H)
		print('K_G',K_G)
		print('K1',K1)
		print('K2',K2)

############################## Needed for Plotting ##################################################

		neighbors = get_neighbors(i,triangles)
		for j,neighbor in enumerate(neighbors):
			for k in range(triangles.shape[0]):
				if len(different_elements(triangles[k],neighbor))==0.0:
					arr_K_G[k]+=K_G
					arr_K_H[k]+=K_H
					arr_K1[k]+=K1
					arr_K2[k]+=K2
					break

	# K_G = np.exp(K_G)
	# K_H = np.exp(K_H)
	# K1 = np.exp(K1)
	# K2 = np.exp(K2)

	np.save('K_H',arr_K_H)
	np.save('K_G',arr_K_G)
	np.save('K1',arr_K1)
	np.save('K2',arr_K2)
	np.save('triangles', triangles)
	np.save('vertices', vertices)