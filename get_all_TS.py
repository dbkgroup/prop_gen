import csv
from calculate_TS import reward_target_molecule_similarity
import rdkit.Chem as Chem
import os
import seaborn as sns
import pickle
from argparse import Namespace
from chemprop.utils import load_args, load_checkpoint, load_scalers
from gym_molecule.envs.molecule import reward_property

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


def getClosestTS(dataset,generated):
    # closest_TS = []
    outfile = 'closest_TS_conditional.csv'
    with open(dataset,'r') as f1:
        with open(generated,'r') as f2:
            reader2 = csv.reader(f2,delimiter=',')
            count=0
            for row2 in reader2:
                if count>=100:
                    break
                f1.seek(0)
                max_TS = -1.0
                max_comp = ''
                reader1 = csv.reader(f1, delimiter=',')
                for row1 in reader1:
                    smile_gen = row2[0]
                    smile_dat = row1[0]
                    mol_gen = Chem.MolFromSmiles(smile_gen)
                    mol_dat = Chem.MolFromSmiles(smile_dat)
                    TS = reward_target_molecule_similarity(mol_gen,mol_dat)
                    # print(TS)
                    if TS > max_TS:
                        max_comp = row1[0]
                    max_TS = max(TS,max_TS)
                    # print(max_TS)
                if max_TS==1:
                    continue
                count+=1
                print(max_TS)
                # closest_TS += [max_TS]
                with open(outfile,'a',newline='') as fts:
                    writer=csv.writer(fts,delimiter=',')
                    writer.writerow([row2[0], max_comp, max_TS])

            # with open('TS.pt','wb') as w:
            #     pickle.dump(closest_TS, w)
            #
            # plot = sns.distplot(closest_TS)
            # plot.figure.savefig('TS_plot.png')

def getConditionalTS(generated):
    # closest_TS = []
    outfile = 'parent_TS_conditional.csv'
    with open(generated,'r') as f:
        with open(outfile, 'w', newline='') as w:
            reader = csv.reader(f,delimiter=',')
            writer = csv.writer(w,delimiter=',')
            i=0
            for row in reader:
                if i>=100:
                    break
                i+=1
                smile = row[0]
                parent = row[1]
                mol_gen = Chem.MolFromSmiles(smile)
                mol_parent = Chem.MolFromSmiles(parent)
                TS = reward_target_molecule_similarity(mol_gen,mol_parent)
                writer.writerow([smile,parent,str(TS)])



def getDensityPlot(dataset,generated):
    closest_TS = []
    with open(dataset,'r') as f1:
        with open(generated,'r') as f2:
            reader2 = csv.reader(f2,delimiter=',')
            count=0
            for row2 in reader2:
                if count>=500:
                    break
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
                count+=1
                print(max_TS)
                closest_TS += [max_TS]

            with open('TS.pt','wb') as w:
                pickle.dump(closest_TS, w)

            plot = sns.distplot(closest_TS)
            plot.figure.savefig('TS_plot.png')

def getPropertyDistribution(dataset):
    with open(dataset,'r') as f:
        property=[]
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            try:
                property+= [float(row[4])]

            except:
                pass

        with open('Property.pt' ,'wb') as w:
            pickle.dump(property,w)

        plot1 = sns.distplot(property, bins=10, kde=False, hist=True)
        plot1.figure.savefig('pki.png')
        plot1.figure.clf()
        plot2 = sns.distplot(property)
        plot2.figure.savefig('pki_density.png')

def getPropertyMulti(model_path):
    infile = 'molecule_multi_test_conditional_final.csv'
    property_dop_multi=[]
    property_norep_multi=[]
    outfile = 'multi_top_500.csv'
    model = load_checkpoint(model_path, cuda=False)
    args = Namespace()
    # print('Loading training args')
    scaler, features_scaler = load_scalers(model_path)
    train_args = load_args(model_path)

    # Update args with training arguments
    for key, value in vars(train_args).items():
        if not hasattr(args, key):
            setattr(args, key, value)
    with open(infile,'r') as f:
        i=0
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            try:
                smile = row[0]
                property_total = float(row[4])
                mol = Chem.MolFromSmiles(smile)
                property_dop = reward_property(model,mol,scaler,features_scaler,train_args,args)

                property_norep = 3*property_dop - property_total
                print(property_dop)
                property_dop_multi+=[property_dop]
                property_norep_multi+=[property_norep]
                print(i)
                if i<500:
                    with open(outfile,'a') as w:
                        writer=csv.writer(w,delimiter=',')
                        writer.writerow([smile,str(property_dop),str(property_norep)])
                i+=1

            except:
                print('B')
                continue

        with open('property_multi_dop.pt','wb') as dop:
            pickle.dump(property_dop_multi,dop)

        with open('property_multi_norep.pt','wb') as norep:
            pickle.dump(property_norep_multi,norep)







if __name__ == "__main__":
    # getTS("N#CC(CCN1CC=C1N)(C1=CC=CC=C1)C1=CC=CC=C1")
    getDensityPlot('dopamine_active_-2.csv','multi_top_500.csv')
    # getPropertyDistribution('dopamine_dataset_load_conditional_final.csv')
    # getClosestTS('dopamine_active_-1.csv', 'load_conditional_top650.csv')
    # getConditionalTS('dopamine_dataset_load_conditional_final.csv')
    # getPropertyMulti('model_hyperopt.pt')