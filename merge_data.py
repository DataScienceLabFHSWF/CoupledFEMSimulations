from hashlib import new
from posixpath import split
import pandas as pd
from glob import glob
import os
from itertools import groupby
import re

def rename_files():
    all_csv = sorted(glob(os.path.join('raw','*.csv')))
    for file in all_csv: 
        new_name = re.sub(r'\.0', '', file)
        if file!=new_name:
            os.rename(file, new_name)


def group_by_paramset():
    all_csv = sorted(glob(os.path.join('raw','*.csv')))
    M1_list = list(filter(lambda k: 'M1' in k, all_csv))
    M2_list = list(filter(lambda k: 'M2' in k, all_csv))
    M3_list = list(filter(lambda k: 'M3' in k, all_csv))
    #templist = list(set(all_csv).symmetric_difference(M1_list))
    M2M3 = M2_list+M3_list

    for filename in M3_list:
        # start of the param set in filenames
        param_set = re.findall(r'WS\d{3,4}_WZ\d{2,3}_p\d\d', filename)[0]
        print(param_set)
        param_set2 = re.findall(r'WS\d{3,4}_WZ\d{2,3}', filename)[0]        
        # groups the filenames by the beginning of their parameter sets
        # concat the lists of filenames to merge
        group = [filename] + [M2_name for M2_name in M2_list if param_set in M2_name] + [M1_name for M1_name in M1_list if param_set2 in M1_name]
        print(group)
        # merge the files and save to disk
        if len(group)>=2:
            df = pd.concat(pd.read_csv(f) for f in sorted(group))
            #name with longest entry from group cause of all params
            merge_name = sorted(group, key=len)[-1][11:-4]
            print(merge_name)
            df.to_csv(os.path.join('merged', 'merged_{}.csv'.format(merge_name)))   
    return 0
   



if __name__ == "__main__":
    rename_files()
    group_by_paramset()