The code is divided into 3 file which resemble the classes created to read an OpenFOAM mesh and data, and multiple examples to show how the classes and VisIT can be used.

------------------------------------------------------
Mesh Class:

Describes the process used to convert an OpenFOAM mesh into a usable Python format.

Data Class:

Describes the process used to read OpenFOAM data and store it in Python format.

Case Class:

Inherts form both Data and Mesh Class, and has a function that outputs the data to a VTK file.


-------------------------------------------------------
Examples:

- Example 1: Is a base case showing how the steps used to convert an OpenFOAM case into Python, and how to simply output the case on VisIt.

- Example 2: Is an extension of Example 1 but shows how to load a case that has data over multiple time steps into VisIT, and how to extract frames from each data file for animation perposes.

- Example 3: Shows how to change the properties when saving a frame .

- Example 4: Shows how to load and control multiple data using the VisIt enviroment.

- Example 5: Demonstrats how to alter the contour attributes.

- Example 6: Demonstrats how to load a 3D case

- Example 7: Demonstrats how to load a 3D case, but make the view 2D

- Example 8: Shows how to use the slice attributes.

- Example 9: Shows how to use the "vector" option in the Addplot command.


