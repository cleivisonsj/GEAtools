# GEATools

This tool aims to improve the results obtained with the NDpredict program in the association of progenitors/descendants of galaxies at different redshifts using the red sequence.

## Pre-requisites

Before using the tool, it is recommended to create a programming environment with Python 3.x.x and R 3.x.x.

You must have the following packages installed in your environment:
- rpy2
- numpy 
- matplotlib 
- h5py 
- pandas 
- scipy 
- xlsxwriter

With Anaconda they can be installed with the command below:
```
conda install -c conda-forge rpy2 numpy matplotlib h5py pandas scipy xlsxwriter
```
In the same folder that the tool files were downloaded should contain the NDpredict (https://github.com/sawellons/NDpredict) and illustris_python (https://github.com/illustristng/illustris_python) libraries. The latter is necessary if working with the data downloaded from the Illustris simulation. It is important to verify the functioning of the libraries following the step-by-step described in the github pages.

In the config.py file, inside the GEATools folder, it is necessary to define the parameters below:
- R_HOME => R root folder path
- R_USER => Path of the root folder of the rpy2 package
- simulation_name => Name of selected Illustris simulation

After that, the tool is ready to use.

## Downloading data from Illustris

The developed tool was tested with Illustris simulation data, and has scripts that help in obtaining the available data.

In the Complementary Scripts folder, with the down_files.py script it is possible to download the data from the Illustris simulations.

Also in this folder, we have the get_subhalo_descendant_tree.py script, necessary to download the descendant trees of the subhalos to be analyzed, in a format compatible with the program. The result of executing this script generates the Auxiliary Data folder, in which the content must be placed in the same folder present in the root of the program.

## Functionalities

The analysis.py script illustrates the basic functioning of the application.

The first step is to import the library by doing:
```
import GEAtools as geat
```

Afterwards, it is necessary to define the snapshot/redshift to be analyzed in z0 and zf and the subhalo id in z0 that will be the chosen progenitor/descendant. In the script this is defined in:
```
snap_num_z0 = 50
snap_num_zf = 53
start_subhalo_z0 = 21 
```

Thus, the result is obtained with NDpredict, doing:
```
prog_subhalo_id = start_subhalo_z0
true_desc_subhalo_id = subhalo_descendant_tree[snap_num_zf]
z0 = redshifts[snap_num_z0]
zf = redshifts[snap_num_zf]
M0 = geat.get_subhalo_mass_star(snap_num_z0, prog_subhalo_id)
sample = geat.get_sample(snap_num_zf, 0)
probs_ndp = geat.calc_prob_ndp(sample, z0, zf, M0)
```

And the result using the red sequence:
```
probs_rg = geat.calc_prob_rg(sample, zf)
geat.adjust_probs_scale(probs_rg)
```

With the result obtained with NDpredict and RG, you can choose the combination method and the weight values, b1 and b2, to combine the results with the objective of improving the probabilities obtained with NDpredict. This is done in the script at:
```
method = 'kk'
kk = []

b1=0.75
b2=0.25
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
```

In the script this is also done for the other available combination methods and weights.

At the end of the script execution, graphs and tables are generated with the results, this information is saved in the Results folder, which is created at the end of the execution.
