from odbAccess import *
import csv
import os
import numpy as np

def extractData(filepath):
    if 'M1' in filepath:
        print('M1')
    # M1
    # Platine beginnt bei 0
    # WZ Matrize beginnt bei: 2672
    # WZ Stempel beginnt bei: 5208
        nodelist=[5208+5,5208+344,2672+304,2672+327,2672+397,8,9,271,238,569]

    elif 'M3' in filepath:
        print('M3')
    # M3=M1
    # Platine beginnt bei 0
    # WZ Matrize beginnt bei: 2672
    # WZ Stempel beginnt bei: 5208    
        nodelist=[5208+5,5208+344,2672+304,2672+327,2672+397,8,9,271,238,569]

    elif 'M2' in filepath:
        print('M2')
    # M2
    # Platine beginnt bei 0
    # WZ Matrize beginnt bei: 2296
    # WZ Stempel beginnt bei: 5656
        nodelist=[5656+5,5656+344,2296+304,2296+327,2296+397,8,9,271,238,569]

    else:
        print('invalid step')

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
            times.append(frame.frameValue)
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
nodelabels="'timestamp', 'Stempel_innen_mitte', 'Stempel_aussen', 'Matrize_zarge_oben', 'Matrize_zarge_mitte','Matrize_zarge_unten', 'Werkstueck_boden', 'Werkstueck_zarge_unten' , 'Werkstueck_zarge_mitte', 'Werkstueck_zarge_oben'"

corrupt_files = []
for file in odbFiles:
    try:
        extractData(file)
    except OdbError:
        corrupt_files.append(file)
        pass
np.savetxt('corrupt_files.txt', np.array(corrupt_files))