# CoupledFEMSimulations

This is the code repository for the paper: 

To generate the input files execute the jupyter notebook file cells.
The corresponding abaqus batchfiles are also generated in the process.

The batch files can then be used with a functioning abaqus installation.

To extract the temperatures at the nodes used in the paper the python script extract_temps.py has to be run on a system where abaqus python is installed: ```abaqus python extract_temps.py```