# DeepGraphMol
This repository serves as the codebase for the paper DeepGraphMol, a multiobjective, computational strategy for generating molecules with desirable properties: a graph convolution and reinforcement learning approach. The code is divided into two sections : <strong> Property Prediction </strong> and <strong> Molecular Generation </strong>

## Property Prediction
We use a Graph Convolutional Network followed by a Feed Forward Network to predict the property scores for molecule. This section of the code is taken from [this wonderful repository](https://github.com/chemprop/chemprop)

### Setup
```bash
 conda install numpy pandas matplotlib
 conda install pytorch torchvision cudatoolkit=10.2 -c pytorch
 conda install -c rdkit rdkit
 ```

### Hyperparameter Optimization
We first try to find optimal hyperparameters using Bayesian Optimization. Currently, the hyperparameters that can be found using this are 1) depth of the GCN encoder 2) the dimensions of the message vectors 3) the number of layers in the Feed Forward Network  4) and the Dropout constant. The code can be run as follows:<br><br>
`python hyperparameter_optimization.py --data_path <data_path> --dataset_type <type> --num_iters <n> --config_save_path <config_path>`<br><br>
where \<data_path\> is the path to csv file where the smiles and the corresponding property scores are stored, \<type\> can be <strong>regression</strong> or <strong>dopamine</strong> which corresponds to using mse loss and adaptive robust loss respectively, \<n\> is the number of epochs and \<config_path\> is the path to json file where the configurations are to be saved. For example: <br><br>
`python hyperparamter_optimization.py --data_path data/dopamine_nodup.csv --dataset_type dopamine --num_iters 100 --config_save_path config.json`

### Training
We can use the configurations obtained from Hyperparameter Optimization or directly train the model by running the following code:<br><br>
`python train.py --data_path <data_path> --dataset_type <type> --save_dir <dir> [--config_path <config_path>]`<br><br>
where \<data_path\> and \<type\> are the same as in case of hyperparameter optimization, \<dir\> is the directory where model is saved, \<config_path\> is the path to json file obtained from running `hyperparameter_optimization.py`. For example:<br><br>
`python train.py --data_path data/dopamine_nodup.csv --dataset_type dopamine --save_dir dop_model --config_path config.json`

### Prediction
The trained model can be used to predict the property scores of molecules using the following:<br><br>
`python predict.py --test_path <test_path> --checkpoint_dir <dir> --preds_path <preds_path>` <br><br>
where \<test_path\> is the path to csv files containing the smiles to be tested, \<dir\> is the directory where the trained model is located \<preds_path\> is the path to csv file where the predictions will be written. For example: <br><br>
`python prpredict.py --test_path data/dopamine_test.csv --checkpoint_dir dop_model --preds_path dopamine_predict.csv`

## Molecular Generation
We use Proximal Policy Optimization (PPO) as the Reinforcement Learning pathway to generate novel molecules having high property score as predicted by the trained model. This model is inspired from the paper [Graph Convolutional Policy Network for Goal-Directed Molecular Graph Generation](https://arxiv.org/abs/1806.02473)

### Setup
- Install the required dependencies
```bash
pip install tensorflow
conda install mpi4py
pip install networkx=1.11
```
- Install OpenAI baseline dependencies
```bash
cd rl-baselines
pip install -e
```
- Install customized gym molecule env
```bash
cd gym-molecule
pip install -e
```
### Run Experiments
This section contains the code to run the 5 experiments as presented in the paper. The general command line argument for running the code is as follows:<br><br>
`mpirun -np <nprocesses> python run_molecule.py --is_conditional <cond_bool>  --reward_type <rew_type> --dataset <dataset> --model_path <m_path> [--model2_path <m2_path> --sa_ratio <sa_ratio> --gan_step_ratio <gstep_ratio> --gan_final_ratio <gfinal_ratio> --conditional <cond_dataset>]`<br><br>
where \<nprocesses\> is the number of parallel processes to be run, \<cond_bool\> is 1 when the generative process is initialized with a molecule else 0, \<rew_type\> is <strong> pki </strong> for single-objective optimization else <strong> multi </strong> for multi-objective optimization, \<dataset\> is <strong>zinc</strong> if taking ZINC as the expert dataset and <strong>dopamine</strong> if taking dopamine BindingDB  as the expert dataset, \<m_path\> is the path to trained model (.pt file), \<m2_path\> is the path to second trained model (.pt file, only valid when reward type is "multi"), \<sa_ratio\> is the weight of SA Score in the final reward, \<gstep_ratio\> is the weight of stepwise discriminator reward in the final reward, \<gfinal_ratio\> is the weight of final discriminator reward in the final reward and \<cond_dataset\> is <strong> dopamine_25 </strong> or <strong> dopamine_15 </strong> which is valid only when \<cond_bool\> is 1.
- <b>Experiment 1</b> <br>
`mpirun -np 8 python run_molecule.py --is_conditional 0  --reward_type pki --dataset zinc --model_path <path_to_dopamine_model> --sa_ratio 2 --gan_step_ratio 2 --gan_final_ratio 3`<br><br>
- <b>Experiment  2</b> <br>
`mpirun -np 8 python run_molecule.py --is_conditional 0  --reward_type pki --dataset dopamine --model_path <path_to_dopamine_model> --sa_ratio 2 --gan_step_ratio 2 --gan_final_ratio 3`<br><br>
- <b>Experiment  3</b> <br>
`mpirun -np 8 python run_molecule.py --is_conditional 1 --conditional dopamine_25  --reward_type pki --dataset zinc --model_path <path_to_dopamine_model> --sa_ratio 2 --gan_step_ratio 2 --gan_final_ratio 3`<br><br>
- <b>Experiment  4</b> <br>
`mpirun -np 8 python run_molecule.py --is_conditional 1 --conditional dopamine_15  --reward_type pki --dataset zinc --model_path <path_to_dopamine_model> --sa_ratio 2 --gan_step_ratio 2 --gan_final_ratio 3`<br><br>
- <b>Experiment  5</b> <br>
`mpirun -np 8 python run_molecule.py --is_conditional 1 --conditional dopamine_25  --reward_type multi --dataset zinc --model_path <path_to_dopamine_model> --model2_path <path_to_norepinephrine_model>  --sa_ratio 2 --gan_step_ratio 2 --gan_final_ratio 3`<br><br>
