from odbAccess import *
import csv
import os
import numpy as np

# v2-publication: node geometry now lives in configs/geometry/{M1,M2,M3}.yaml
# and is loaded by geometry.resolve_geometry(). Editing the mesh no longer
# requires touching this script.
from geometry import resolve_geometry, csv_header


def extractData(filepath):
    geom = resolve_geometry(filepath)
    print(geom.name)
    nodelist = geom.nodelist
    if geom.start_time_source == "zero":
        start_time = 0
    else:
        # M2/M3 chain onto the previous tool's last timestamp; `times` is
        # populated by the previous extractData call in the outer loop.
        start_time = times[-1]

    nodelabels = csv_header(geom)

    #open odb file
    odb = openOdb(filepath)
    print('Extracting Data from {}'.format(filepath))
    #make a matrix to store data of size history x nodes
    rows=0
    for step in odb.steps.keys():
        # add all frames for each step
        rows+=len(odb.steps[step].frames)
    cols = len(nodelist) # len(odb.steps['Step-1'].frames[-1].fieldOutputs['TEMP'].values) 
    shape=(rows,cols)
    data = np.zeros(shape)
    #iterate over all steps
    times= []

    for step in odb.steps.keys():
        # iterate over all frames (history)        
        for i in range(len(odb.steps[step].frames)):
            frame=odb.steps[step].frames[i]
            NodetempValues=frame.fieldOutputs['TEMP'].values
            times.append(frame.frameValue + start_time)
            #iterate over each node
            #for j in range(len(NodetempValues)):
            for j, node in enumerate(nodelist):
                data[i][j] =  NodetempValues[node].data

    times = np.array(times)
    data = np.column_stack((times, data))
    print('saving to ' + 'raw' + '{}.csv'.format(os.path.splitext(filepath)[0]))
    np.savetxt(os.path.join('raw','{}.csv'.format(os.path.splitext(filepath)[0])), data, header=nodelabels, delimiter=",", comments='')

# durchlaufend nummeriert?
# unterschiedlich fuer M1, M2 und M3

odbFiles= [os.path.join('FEM_SIMS', f) for f in os.listdir('FEM_SIMS') if f.endswith(".odb")]
print(len(odbFiles))

corrupt_files = []
for file in odbFiles:
    try:
        extractData(file)
    except OdbError:
        corrupt_files.append(file)
        pass
np.savetxt('corrupt_files.txt', np.array(corrupt_files))