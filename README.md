# diffGeoOps

This project implements the following paper

> http://multires.caltech.edu/pubs/diffGeoOps.pdf

Every folder in the project mainly consists of:
* The _off_ files for the meshes.
* File curvature.py
* File plot.py

The file __curvature.py__ implements the algorithm mentioned in the paper and stores the curvature values at each vertex of the triangular mesh as a numpy array.

The file __plot.py__ shows the plots of the meshes with color scheme according to the value of curvatures. 
In order to plot, go to the directory of the mesh and just run the file plot.py.

The following libraries are used
* numpy
* mayavi (for plotting)

## License 

Copyright (c) 2019 Pranav Jain

For license information, see [LICENSE](LICENSE) or http://mit-license.org


- - -

This code was written as a part of my independent study in **Differential Geometry** with [Dr. Kaushik Kalyanaraman](https://www.iiitd.ac.in/kaushik) at IIIT Delhi during Winter 2019 Semester. 

For bugs in the code, please write to: pranav16255 [at] iiitd [dot] ac [dot] in
