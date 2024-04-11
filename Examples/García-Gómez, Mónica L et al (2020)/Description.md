# Identification of multivalued refinements of the model of stem cell division in the Root of Arabidopsis thaliana

To run the code the “inputs.py”  and “ASYN.bnet” files must be in the MRBM folder. 

## Identification of components to be multivalued
We seek a multivalued refinement whose asyncrhonous dynamics leads to specific sizes of basin of attraction (similar to those in the most permissive dynamics of the Boolean model). The first step consist on identifying the the set J of mp node necessary to recover the target size of basin of attraction in the partial J mp dynamics. To do so we use the code `1.multivalued_nodes_identification.py`. 
The code generate several outputs:

- FINAL_PARTIAL_SETS_J.txt: List of sets J that allow to recover part of the basin of attraction sizes
- FINAL_SETS_J.txt: List of set J that recover all the desired basin of attraction size
- TARGET_MP_BASIN.txt: List of the basin (configuration of the attractor and its size) that are initialy different between the asynchronous and mp dynamics
- SS.json: dict of the attracts configuation whose size we want to recover.

## Identification of multivalued refinement(s)
All the output will be used as inputs for the second code `2.refinement_identification.py`.
