# Identification of Multivalued Refinements of the Boolean Model of Asymmetric Stem Cell Division in *Arabidopsis Thaliana* Root

To run the code, the “inputs.py” and “ASYN.bnet” files must be in the MRBM folder.

## Identification of components to be multivalued
Command used: `python 1.multivalued_nodes_identification.py -mn AT -p b`

We seek a multivalued refinement whose asynchronous dynamics leads to specific sizes of basin of attraction (similar to those in the most permissive dynamics of the Boolean model). The first step consists of identifying the set J of mp nodes necessary to recover the target size of basin of attraction in the partial J mp dynamics. To do so, we use the code `1.multivalued_nodes_identification.py`. 
The code generates several outputs:

- FINAL_PARTIAL_SETS_J.txt: List of sets J that allow recovering part of the basin of attraction sizes.
- FINAL_SETS_J.txt: List of set J that recover all the desired basin of attraction size.
- TARGET_MP_BASIN.txt: List of configurations of attractors and the size of their basin of attraction that are initially different between the asynchronous and mp dynamics.
- SS.json: Dict of the attractor configurations whose size we want to recover.

We identified only one set J for which the partial Jm.p. dynamics led to the size of basin of attraction similar to those in the m.p. dynamics: [["MGP", "SCR", "SHR"]]. We identified several sets J that recover part of the size of basin of attraction, the recovered condiguration (separated by "-" if several are recovered) for specific set J are  the following: 
- "111010000010101001": [["JKD"], ["SCR"]],
- "111110110010100001": [["SHR"]],
- "111010000010101001-111110110010100001": [["JKD", "SHR"], ["SCR", "SHR"]],
- "101010001010111011-111010000010101001": [["MGP", "SCR"]].

We used all of those sets J in the second part to identify a multivalued refinement whose asynchronous dynamics would lead to the target size of basin of attraction. In those models, the sets J correspond to the multivalued nodes.

## Identification of multivalued refinement(s)
Run the following command: `python 2.refinement_identification.py -mn AT -p b -m c`. 
We run this command for several sets J (change path to the file containing the set J to test) in order to test every possible parameterization of multivalued refinements to check if their asynchronous dynamics leads to the target size of basin of attraction. We run the test with a maximal level of activity for a multivalued node equal to 2 (it's the default).
