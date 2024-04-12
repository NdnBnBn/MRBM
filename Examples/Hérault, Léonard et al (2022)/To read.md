# Identification of Multivalued Refinements of HSC Aging in Human

To execute the code, ensure that the “inputs.py” and “ASYN.bnet” files are placed in the MRBM folder.

## Identification of Components for Multivalued Analysis
Command used: `python 1.multivalued_nodes_identification.py -mn ML -p r`

We aim to identify a multivalued refinement whose asynchronous dynamics can capture specific reachabilities (as specified in the inputs.py file), observable only in the most permissive (m.p.) dynamics of the Boolean model. Initially, we identify the set(s) J of m.p. nodes necessary to recover the target basin of attraction size in the partial J m.p. dynamics. We achieve this using the code `1.multivalued_nodes_identification.py`. 
The following outputs are obtained:
- FINAL_PARTIAL_SETS_J.txt: Lists of sets J that partially recover the reachabilities.
- FINAL_SETS_J.txt: List of set J that fully recovers all the desired reachabilities.
- TARGET_REACH.txt: Reachability to be recovered in the multivalued refinement.
- REACH_RES: Configuration of the states (initial state and state to reach).

We identified only one set J for which the partial J m.p. dynamics recovers all the desired reachabilities: [["Egr1", "Fli1", "Gata1", "Gata2"]]. Additionally, several sets J partially recover them (reachability names separated by "-" and the corresponding set J): 
- pME_pEr-preDiff_pEr: [["Fli1"]],
- srHSC_pLymph: [["Gata2"], ["Spi1"]],
- iHSC_pLymph-srHSC_pLymph: [["Egr1", "Gata2"], ["Egr1", "Spi1"], ["Gata1", "Gata2"], ["Gata2", "Junb"], ["Junb", "Spi1"]],
- pME_pEr-preDiff_pEr-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1"]],
- pME_pEr-preDiff_pEr-srHSC_pLymph: [["Fli1", "Gata2"], ["Fli1", "Spi1"]],
- pME_pEr-preDiff_pEr-iHSC_pLymph-srHSC_pLymph: [["Egr1", "Fli1", "Gata2"], ["Egr1", "Fli1", "Spi1"], ["Fli1", "Gata2", "Junb"], ["Fli1", "Junb", "Spi1"]],
- pME_pEr-preDiff_pEr-iHSC_pLymph-srHSC_pLymph-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1", "Gata2"]],
- pME_pEr-preDiff_pEr-srHSC_pLymph-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1", "Spi1"]].

All these sets J are utilized in the subsequent step to identify a multivalued refinement capable of capturing the target reachabilities. In these models, the sets J represent the multivalued nodes.

## Identification of Multivalued Refinement(s)
Execute the following command: `python 2.refinement_identification.py -mn ML -p r -m p`. 
The output is saved in a text file named "ML_path_generated_rules.txt".

The output consists of regulatory functions describing the activation conditions of nodes regulated by multivalued nodes ("Egr1", "Fli1", "Gata1", and "Gata2") to recover paths corresponding to the reachability of interest in the partial J m.p. dynamics (with J = {"Egr1", "Fli1", "Gata1", "Gata2"}). For each multivalued node, the regulation level is denoted by "_level". For example: Gata1 at level 2 will be denoted as Gata1_2. 

By comparing this output to the rules of the initial Boolean model, we inferred the following possible rules:

- Cebpa: (!Ikzf1 & Gata2) | (!Ikzf1 & Spi1)
- Egr1: Gata2_2 | Junb
- Fli1: (Junb) | (!Klf1 & Gata1_2)
- Gata1: Fli1 | (Gata2 & !Spi1) | (Gata1 & !Ikzf1 & !Spi1)
- Gata2: (Gata2 & !Gata1 & !Zfpm1) | (Egr1 & !Gata1 & !Zfpm1 & !Spi1)
- Ikzf1: Gata2_2
- Junb: Myc | Egr1_2
- Klf1: Gata1 & !Fli1_2
- Spi1: (Spi1 & !Gata1_2) | (Cebpa & !Gata1_2 & !Gata2_2)
- Tal1: Gata1_2 & !Spi1
- Zfpm1: Gata1
