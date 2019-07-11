import csv
import rdkit.Chem as Chem

infile = '250k_rndm_zinc_drugs_clean.smi'
outfile = 'zinc_without_p.csv'

with open(infile,'r') as f:
    with open(outfile,'a',newline='') as w:
        reader = csv.reader(f,delimiter=',')
        writer = csv.writer(w,delimiter=',')
        for line in reader:
            smile = line[0]
            if 'p' in smile or 'P' in smile:
                continue
            else:
                writer.writerow([smile])