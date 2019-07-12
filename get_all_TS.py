import csv
from calculate_TS import reward_target_molecule_similarity
import rdkit.Chem as Chem
import os
import seaborn as sns
import pickle

def getTS(smile):
    mol = Chem.MolFromSmiles(smile)
    infile = 'dopamine_nodup.csv'
    outfile = os.path.join('dopamine_ts', str(smile)+'_TS.csv')
    with open(infile,'r') as f:
        with open(outfile,'a',newline='') as w:
            reader = csv.reader(f,delimiter=',')
            writer = csv.writer(w,delimiter=',')
            for row in reader:
                target = Chem.MolFromSmiles(row[0])
                TS = reward_target_molecule_similarity(mol,target)
                writer.writerow([row[0], str(TS), str(row[1])])


def getDensityPlot(dataset,generated):
    closest_TS = []
    with open(dataset,'r') as f1:
        with open(generated,'r') as f2:
            reader2 = csv.reader(f2,delimiter=',')
            for row2 in reader2:
                f1.seek(0)
                max_TS = -1.0
                reader1 = csv.reader(f1, delimiter=',')
                for row1 in reader1:
                    smile_gen = row2[0]
                    smile_dat = row1[0]
                    mol_gen = Chem.MolFromSmiles(smile_gen)
                    mol_dat = Chem.MolFromSmiles(smile_dat)
                    TS = reward_target_molecule_similarity(mol_gen,mol_dat)
                    # print(TS)
                    max_TS = max(TS,max_TS)
                    # print(max_TS)
                if max_TS==1:
                    continue
                # print(max_TS)
                closest_TS += [max_TS]

            with open('TS.pt','wb') as w:
                pickle.dump(closest_TS, w)

            plot = sns.distplot(closest_TS)
            plot.figure.savefig('TS_plot.png')




if __name__ == "__main__":
    # getTS("N#CC(CCN1CC=C1N)(C1=CC=CC=C1)C1=CC=CC=C1")
    getDensityPlot('dopamine_nodup_active.csv','molecule_dopamine_test_conditional_load_conditional.csv')
