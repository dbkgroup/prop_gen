import csv
import rdkit.Chem as Chem

infile = 'multi_dataset.csv'
outfile = 'multi_obj_dataset.csv'

with open(infile,'r') as f:
    with open(outfile,'a',newline='') as w:
        reader = csv.reader(f,delimiter=',')
        writer = csv.writer(w,delimiter=',')
        for line in reader:
            m = Chem.MolFromSmiles(str(line[0]))
            if m.GetNumAtoms() < 55:
                writer.writerow([line[0]])
