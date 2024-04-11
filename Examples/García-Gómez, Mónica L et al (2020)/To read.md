# Identification of Multivalued Refinements of the Boolean Model of Asymmetric Stem Cell Division in *Arabidopsis Thaliana* Root

To run the code the “inputs.py”  and “ASYN.bnet” files must be in the MRBM folder. 

## Identification of components to be multivalued
Command used: `python 1.multivalued_nodes_identification.py -mn AT -p b -M 5`

We seek a multivalued refinement whose asyncrhonous dynamics leads to specific sizes of basin of attraction (similar to those in the most permissive dynamics of the Boolean model). The first step consist on identifying the the set J of mp node necessary to recover the target size of basin of attraction in the partial J mp dynamics. To do so we use the code `1.multivalued_nodes_identification.py`. 
The code generate several outputs:

- FINAL_PARTIAL_SETS_J.txt: List of sets J that allow to recover part of the basin of attraction sizes
- FINAL_SETS_J.txt: List of set J that recover all the desired basin of attraction size
- TARGET_MP_BASIN.txt: List of configuration of attractor and the size of it basin of attraction that are initialy different between the asynchronous and mp dynamics
- SS.json: dict of the attracts configuation whose size we want to recover.

## Identification of multivalued refinement(s)
All the output will be used as inputs for to run the following comand: `python 2.refinement_identification.py -mn AT -p b -m c` 
