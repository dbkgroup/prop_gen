# GraphMol
This repository serves as the codebase for the paper GraphMol: GraphMol, a multiobjective, computational strategy for generating molecules with desirable properties: a graph convolution and reinforcement learning approach. The code is divided into two sections : <strong> Property Prediction </strong> and <strong> Molecular Generation </strong>

## Property Prediction
We use a Graph Convolutional Network followed by a Feed Forward Network to predict the property scores for molecule. This section of the code is taken from [this wonderful repository](https://github.com/chemprop/chemprop)

### Hyperparameter Optimization
We first try to find optimal hyperparameters using Bayesian Optimization. Currently, the hyperparameters that can be found using this are 1) depth of the GCN encoder 2) the dimensions of the message vectors 3) the number of layers in the Feed Forward Network  4) and the Dropout constant. The code can be run as follows:<br>
`python hyperparameter_optimization.py --data_path <data_path> --dataset_type <type> --num_iters <n> --config_save_path <config_path>`<br>
where \<data_path\> is the path to csv file where the smiles and the corresponding property scores are stored, \<type\> can be <strong>regression</strong> or <strong>dopamine</strong> which corresponds to using mse loss and adaptive robust loss respectively, \<n\> is the number of epochs and \<config_path\> is the path to json file where the configurations are to be saved. For example: <br>
`python hyperparamter_optimization.py --data_path dopamine_nodup.csv --dataset_type dopamine --num_iters 100 --config_save_path config.json`

### Training
We can use the configurations obtained from Hyperparameter Optimization or directly train the model by running the following code:<br>
`python train.py --data_path <data_path> --dataset_type <type> --save_dir <dir> [--config_path <config_path>]`<br>
where \<data_path\> and \<type\> are the same as in case of hyperparameter optimization, \<dir\> is the directory where model is saved, \<config_path\> is the path to json file obtained from running `hyperparameter_optimization.py`. For example:<br>
`python train.py --data_path dopamine_nodup.csv --dataset_type dopamine --save_dir dop_model --config_path config.json`
