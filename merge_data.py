import pandas as pd
from glob import glob
import os
from itertools import groupby
import re

def group_by_paramset():
    all_csv = sorted(glob(os.path.join('raw','*.csv')))

    for filename in all_csv:
        # start of the param set in filenames
        param_set = str(filename[11:23])

        # groups the filenames by the beginning of their parameter sets
        split_csv = [ list(i) for j, i in groupby(all_csv, lambda a: re.split(r'WTP-M\d_{}'.format(param_set), a)[0])]

        # merge the files if all 3 steps are in the group
        for group in split_csv:
            if len(group)>=2:
                df = pd.concat(pd.read_csv(f) for f in group)
                #name with longest entry from group cause of all params
                merge_name = sorted(group, key=len)[-1][11:-4]
                df.to_csv(os.path.join('merged', 'merged_{}.csv'.format(merge_name)))   
    return 0
   

if __name__ == "__main__":
    group_by_paramset()