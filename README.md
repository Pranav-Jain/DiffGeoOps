# Curvatures-of-Triangulated-2-Manifolds

This project implements the following paper

http://www.geometry.caltech.edu/pubs/DMSB_III.pdf

Every folder in the project mainly consists of:
* The _off_ files for the meshes.
* File curvature.py
* File plot.py

The file __curvature.py__ implements the algorithm mentioned in the paper and storees the curvature values at each vertex of the triangular mesh as a numpy array.

The file __plot.py__ shows the plots of the meshes with color scheme according to the value of curvatures. 
In order to plot, go to the directory of the mesh and just run the file plot.py.

The following libraries are used
* numpy
* mayavi (for plotting)
