import csv
import rdkit.Chem as Chem

infile = 'dopamine_active_dataset.csv'
outfile = 'smiles_active_conditional.csv'

with open(infile,'r') as f:
    with open(outfile,'a',newline='') as w:
        reader = csv.reader(f,delimiter=',')
        writer = csv.writer(w,delimiter=',')
        for line in reader:
            m = Chem.MolFromSmiles(str(line[0]))
            if m.GetNumAtoms() < 25:
                writer.writerow([line[0]])
