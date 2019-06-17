import csv
import os
from rdkit import Chem
from gym_molecule.envs.molecule import reward_penalized_log_p

filename = "molecule_zinc_test_conditional.csv"
outname = "property.csv"
if os.path.exists(outname):
    os.remove(outname)
with open(filename,'r') as f:
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        if len(row)==0:
            continue
        if Chem.MolFromSmiles(row[0]) is not None:
            with open(outname,'a',newline='') as w:
                writer = csv.writer(w,delimiter=',')
                # print(row[0])
                # print(reward_penalized_log_p(Chem.MolFromSmiles(row[0])))
                try:
                    writer.writerow([row[0], str(reward_penalized_log_p(Chem.MolFromSmiles(row[0])))])
                except:
                    pass


