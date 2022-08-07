# Generate section and material files | Author: Mauro Francisco Arcidiacono

# This script creates the section and material input files. This code is the result  
# of translating to Python 3 the original Matlab code developed by Dylan Agius. 

# Purpose
# Create a microstructure using Neper, with the output of the microstructure
# format as an Abaqus input file and update the Abaqus input file to include
# materials and sections for each generated grain.

# The purpose of including the volume and seed information is to calculate 
# the equivalent spherical diameter of each grain and the centroid location 
# which are used by a UMAT to determine the location of the integration
# point with respect to the grain boundary.

# How to use
# Run python neper2abq.py in the command line. The input file name considered
# is input_file_info.xlsx and can be changed by modifying the xls variable 
# definition in this script.

# Import libraries.
import pandas as pd
import numpy as np
import math

# Import the input Excel file and read the tabs: euler angles, centroid coordinates and set volume.
xls = pd.ExcelFile('input_file_info.xlsx')
eulera = pd.read_excel(xls, 'orientations', header=None)
centroid = pd.read_excel(xls, 'seed', header=None)
volume = pd.read_excel(xls, 'volume', header=None)

# Calculate the equivalent spherical diameter.
diameq = [(6*volume._get_value(i,0)/math.pi)**(1/3) for i in range(len(eulera.index))]

# Create the transformation matrices. 
zrot = []
xrot = []
zrot2 = []
total_rot = []

for i in range(len(eulera.index)):
    
    cos1 = math.cos(np.radians(eulera[0][i]))
    sin1 = math.sin(np.radians(eulera[0][i]))
    
    cos2 = math.cos(np.radians(eulera[1][i]))
    sin2 = math.sin(np.radians(eulera[1][i]))
    
    cos3 = math.cos(np.radians(eulera[2][i]))
    sin3 = math.sin(np.radians(eulera[2][i]))
    
    zrot.append(np.array([[cos1, sin1, 0], [-sin1, cos1, 0], [0, 0, 1]]))
    xrot.append(np.array([[1, 0, 0], [0, cos2, sin2], [0, -sin2, cos2]]))
    zrot2.append(np.array([[cos3, sin3, 0], [-sin3, cos3, 0], [0, 0, 1]]))
    total_rot.append(np.transpose(zrot2[i]@xrot[i]@zrot[i]))

# Define vectors in the local coordinate system.
vecs1 = np.array([1, 0, 0])
vecs2 = np.array([0, 1, 0])

# Rotate local vectors to global system using the transformation matrices.
rotvec1 = []
rotvec2 = []

for i in range(len(eulera.index)):
    rotvec1.append(total_rot[i]@vecs1)
    rotvec2.append(total_rot[i]@vecs2)

# Write the sections input file.
sections_file = open('input_file_info.xlsx_sections.inp' , 'w')

for i in range(1, len(eulera.index)+1):
    sections_file.write(f"**Section: Section_Grain_Mat{i}\n*Solid Section, elset=poly{i}, material=Grain_Mat{i}\n,\n")

# Write the materials input file.
materials_file = open('input_file_info.xlsx_materials.inp' , 'w')

matParams = pd.read_excel(xls, 'Material_parameters', header=None)

if len(matParams.index)<168:
    for k in range(160, 176):
        matParams.loc[k, 0] = 0
else:
    for k in range(168, 176):
        matParams.loc[k, 0] = 0
matParams.loc[56:58, 0] = vecs1
matParams.loc[64:66, 0] = vecs2

for i in range(len(eulera.index)):
    index1 = 0
    index2 = 8
    materials_file.write(f"\n*Material, name=Grain_Mat{i+1}\n*Depvar\n10000,\n*User Material, constants=175\n")
    matParams.loc[59:61, 0] = rotvec1[i]
    matParams.loc[67:69, 0] = rotvec2[i]
    matParams.loc[168:170, 0] = np.radians([eulera[0][i],eulera[1][i],eulera[2][i]])
    matParams.loc[171:173, 0] = [centroid[0][i],centroid[1][i],centroid[2][i]]
    matParams.loc[174, 0] = diameq[i]
    for j in range(0, 21):
        materials_file.write(f"""{round(matParams[index1:index2][0][index1], 7)}, {round(matParams[index1:index2][0][index1+1], 7)}, \
{round(matParams[index1:index2][0][index1+2], 7)}, {round(matParams[index1:index2][0][index1+3], 7)}, \
{round(matParams[index1:index2][0][index1+4], 7)}, {round(matParams[index1:index2][0][index1+5], 7)}, \
{round(matParams[index1:index2][0][index1+6], 7)}, {round(matParams[index1:index2][0][index1+7], 7)}\n""")
        index1 += 8
        index2 += 8
    materials_file.write(f"""{round(matParams[index1:index2][0][index1], 7)}, {round(matParams[index1:index2][0][index1+1], 7)}, \
{round(matParams[index1:index2][0][index1+2], 7)}, {round(matParams[index1:index2][0][index1+3], 7)}, \
{round(matParams[index1:index2][0][index1+4], 7)}, {round(matParams[index1:index2][0][index1+5], 7)}, \
{round(matParams[index1:index2][0][index1+6], 7)}, {round(matParams[index1:index2][0][index1+7], 7)}""")

# Close the files.
sections_file.close()
materials_file.close()
xls.close()