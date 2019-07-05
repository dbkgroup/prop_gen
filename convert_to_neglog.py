import csv
import numpy as np
import os
infile = "norep_ki_nodup.csv"
outfile = "norep_pki_nodup.csv"
if os.path.exists(outfile):
    os.remove(outfile)
with open(infile, 'r', newline='') as f:
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        with open(outfile, 'a', newline='') as w:
            writer = csv.writer(w, delimiter=',')
            writer.writerow([row[0], str(-1*np.log10(float(row[1])))])


