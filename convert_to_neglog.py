import csv
import numpy as np
import os
infile = "dopamine_processed.csv"
outfile = "dopamine.csv"
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
            writer.writerow([row[0], str(-1*np.log10(float(row[1])))])
            i += 1


