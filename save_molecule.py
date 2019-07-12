import csv
import rdkit.Chem as Chem
import rdkit.Chem.Draw as Draw

infile = 'molecule_dopamine_test_conditional_load_conditional.csv'
with open(infile,'r') as f:
    reader = csv.reader(f,delimiter=',')
    i = 0
    for j in range(8):
        next(reader)
    for row in reader:
        smile1 = row[0]
        smile2 = row[1]
        mol1 = Chem.MolFromSmiles(smile1)
        mol2 = Chem.MolFromSmiles(smile2)
        Draw.MolToFile(mol1,str(i) + '_' + str(row[4]) + '_'+'_mol_.png')
        Draw.MolToFile(mol2,str(i) + '_' + str(row[4]) + '_' + 'parent.png')
        i+=1
        if i>15:
            break


