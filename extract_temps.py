from odbAccess import *
import csv
from os import listdir
from os.path import isfile, join, splitext
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
    for step in odb.steps.keys():
        # iterate overv all frames (history)
        for i in range(len(odb.steps[step].frames)):
            frame=odb.steps[step].frames[i]
            NodetempValues=frame.fieldOutputs['TEMP'].values
            #iterate over each node
            #for j in range(len(NodetempValues)):
            for j, node in enumerate(nodelist):
                data[i][j] =  NodetempValues[node].data

    print('saving to ' + 'output' + '{}.csv'.format(splitext(filepath)[0]))
    np.savetxt(join('output','{}.csv'.format(splitext(filepath)[0])), data, header=nodelabels, delimiter=",", comments='')

# durchlaufend nummeriert?
# unterschiedlich fuer M1, M2 und M3

odbFiles= [join('test', f) for f in listdir('test') if isfile(join('test', f))]
print(odbFiles)
nodelabels="'Stempel_innen_mitte', 'Stempel_aussen', 'Matrize_zarge_oben', 'Matrize_zarge_mitte','Matrize_zarge_unten', 'Werkstueck_boden', 'Werkstueck_zarge_unten' , 'Werkstueck_zarge_mitte', 'Werkstueck_zarge_oben'"

for file in odbFiles:
    extractData(file)
