import csv
import rdkit.Chem as Chem
import rdkit.Chem.Draw as Draw
import os

infile = 'multi_top_500.csv'
with open(infile,'r') as f:
    reader = csv.reader(f,delimiter=',')
    i = 0
    for row in reader:
        smile1 = row[0]
        # smile2 = row[1]
        mol1 = Chem.MolFromSmiles(smile1)
        # mol2 = Chem.MolFromSmiles(smile2)
        Draw.MolToFile(mol1,os.path.join('Multi Molecules',str(i) + '_' + str(row[1]) + '_'+'mol.png'))
        # Draw.MolToFile(mol2,os.path.join('Multi Molecules',str(i) + '_' + str(row[2]) + '_' + 'closest.png'))
        i+=1
        if i>50:
            break


