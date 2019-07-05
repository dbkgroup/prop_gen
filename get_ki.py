import csv
import numpy as np
import os
infile = "norep.csv"
outfile = "norep_ki.csv"
if os.path.exists(outfile):
    os.remove(outfile)
with open(infile, 'r', newline='') as f:
    i=0
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        with open(outfile, 'a', newline='') as w:
            if i == 0:
                i += 1
                continue
            writer = csv.writer(w, delimiter=',')
            if row[1] is not None and row[1]!='':
                if row[1][0] =='>' or row[1][0]=='<':
                    writer.writerow([row[0], row[1][1:]])
                else:
                    writer.writerow([row[0],row[1]])
            elif row[2] is not None and row[2]!='':
                if row[2][0] =='>' or row[2][0]=='<':
                    writer.writerow([row[0], row[2][1:]])
                else:
                    writer.writerow([row[0],row[2]])
            # writer.writerow([row[0], str(-1*np.log10(float(row[1])))])
            i += 1


