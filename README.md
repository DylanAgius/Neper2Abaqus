# Neper2Abaqus
## Main Function
Create a microstructure using Neper, with the output of the microstructure format as an Abaqus input file and update the Abaqus input file to include materials and sections for each generated grain.

The purpose of including the volume and seed information is to calculate the equivalent spherical diameter of each grain and the centroid location which are used by the current UMAT to determine the location of the integration point with respect to the grain boundary.

The functionality has been extended thanks to [Mauro Arcidiacono](https://github.com/mauroarcidiacono) who has now extended the tool to Python making it much easier for open source users to take advantage of this tool.

## Creating Microstruture with Neper
Included here is an example shell file (neper_example.sh) which can be used to create a synthetic microstructre in Neper with the following features:
* a unit volume RVE with 300 grains.
* assigned angles defined by euler angles
### Extracting information output from Neper
The grain information can be extracted from the file '.tess' generated by Neper.
The important information to use here are:
* orientation (found at the location in the file marked with 'ori')
* grain centroid in x,y,z (found at the location in the file marked with 'seed' using the 2nd-4th columns)

The volume for each grain is found in the file with extension '.stelset'

Once this information is extracted, it all should be added to the corresponding sheets in the excel file included here named 'input_file_info'

## Material parameters
The material parameters required should also be added to the corresponding sheet in the excel file named 'input_file_info'.  The parameters from 1-155 are based on the order in the pdf file found in this repository (Huang - 1991 - A User-Material Subroutine Incorporating Single Crystal Plasticity in the ABAQUS Finite Element Program -- MECH-178.pdf).

## Installation
Simply copy files in the folder titled *Neper2Abaqus* into the MATLAB file path.

## Running the MATLAB function
Run using from the command line using: neper2abq('name__') where 'name' is the name of the input file.  Please also include the double underscore at the end of the name you choose.

Running this function will create two files:
* 'name_materials.inp'
* 'name_sections.inp'

## Creating the final input file for Abaqus
The final step is to take the input file generated by Neper and the two input files created using this function and add them to the same folder.  Finally, open the input file generated by Neper and modify in by adding to the end of the file the following:

* Before'\*End Part':

  \*Include, Input = name_sections.inp

* After '\*End Part':

  \*Include, Input = name_materials.inp

This input file can now by imported into Abaqus with the model containing all the materials and sections.

## Contributing
If you make changes to improve the capability, please don't hesitate to create a pull request and I'll recognise your contribution.
