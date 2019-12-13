# Neper2Abaqus
## Main Function
Create a microstructure using Neper, with the output of the microstructure format as an Abaqus input file and update the Abaqus input file to include materials and sections for each generated grain
## Creating Microstruture with Neper
Included here is an example shell file which can be used to create a synthetic microstructre in Neper with the following features:
* a unit volume RVE with 300 grains.
* assigned angles defined by euler angles
* volume of each grain is outputed with extension '.stelset'
### Extracting information output from Neper
The grain information can be extracted from the file '.tess' generated by Neper.
The important information to use here are:
* orientation
