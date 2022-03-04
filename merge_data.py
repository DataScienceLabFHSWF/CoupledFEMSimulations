from posixpath import split
import pandas as pd
from glob import glob
import os
from itertools import groupby
import re

def group_by_paramset():
    all_csv = sorted(glob(os.path.join('raw','*.csv')))
    M3_list = list(filter(lambda k: 'M3' in k, all_csv))
    # make a temporary XOR list
    templist = list(set(all_csv).symmetric_difference(M3_list))
    
    for filename in M3_list:
        # start of the param set in filenames
        param_set = str(filename[11:26])
        print(param_set)
        # groups the filenames by the beginning of their parameter sets
        # merge 1 and 2 first then 3
        split_csv = [ list(i) for j, i in groupby(templist, lambda a: re.split(r'WTP-M\d_{}'.format(param_set), a)[0])]
        # merge the files if all 3 steps are in the group
        for group in split_csv:
            if len(group)==2:
                #if M1 and M2 fit together append the fitting M3 and concat
                group.append(filename)
                df = pd.concat(pd.read_csv(f) for f in sorted(group))
                #name with longest entry from group cause of all params
                merge_name = sorted(group, key=len)[-1][11:-4]
                df.to_csv(os.path.join('merged', 'merged_{}.csv'.format(merge_name)))   
    return 0
   

if __name__ == "__main__":
    group_by_paramset()