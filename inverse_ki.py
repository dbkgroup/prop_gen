import csv
import numpy as np
import os
infile = "dopamine_processed.csv"
outfile = "dopamine_inverse.csv"
if os.path.exists(outfile):
    os.remove(outfile)
with open(infile, 'r', newline='') as f:
    reader = csv.reader(f,delimiter=',')
    next(reader)
    for row in reader:
        with open(outfile, 'a', newline='') as w:
            writer = csv.writer(w, delimiter=',')
            writer.writerow([row[0], str(1/float(row[1]))])


