# Identification of Multivalued Refinements of HSC agin in humain

To run the code, the “inputs.py” and “ASYN.bnet” files must be in the MRBM folder.

## Identification of components to be multivalued
Command used: `python 1.multivalued_nodes_identification.py -mn ML -p r`

We seek a multivalued refinement whose asynchronous dynamics specific reachabilities (given in the inputs.py file) only observable in the m.p. dynamics of the Boolean model. 
First we identify the set(s) J of m.p. nodes necessary to recover the target size of basin of attraction in the partial J m.p. dynamics. To do so, we use the code `1.multivalued_nodes_identification.py`. 
We oubtain the following outputs:
- FINAL_PARTIAL_SETS_J.txt: List of sets J that allow recovering part of the reachabilities.
- FINAL_SETS_J.txt: List of set J that recover all the desired reachabilities.
- TARGET_REACH.txt: rechability to recover in the multivalued refinement.
- REACH_RES: configuration of the states (initatial state, and state to reach).

We identified only one set J for which the partial Jm.p. dynamics recovers the totality of the reachabilities desired: [["Egr1", "Fli1", "Gata1", "Gata2"]]. We identified several sets J that recover part of them (name of the rechability seprated by "-" and the set J): 
- pME_pEr-preDiff_pEr: [["Fli1"]],
- srHSC_pLymph: [["Gata2"], ["Spi1"]],
- iHSC_pLymph-srHSC_pLymph: [["Egr1", "Gata2"], ["Egr1", "Spi1"], ["Gata1", "Gata2"], ["Gata2", "Junb"], ["Junb", "Spi1"]],
- pME_pEr-preDiff_pEr-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1"]],
- pME_pEr-preDiff_pEr-srHSC_pLymph: [["Fli1", "Gata2"], ["Fli1", "Spi1"]],
- pME_pEr-preDiff_pEr-iHSC_pLymph-srHSC_pLymph: [["Egr1", "Fli1", "Gata2"], ["Egr1", "Fli1", "Spi1"], ["Fli1", "Gata2", "Junb"], ["Fli1", "Junb", "Spi1"]],
- pME_pEr-preDiff_pEr-iHSC_pLymph-srHSC_pLymph-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1", "Gata2"]],
- pME_pEr-preDiff_pEr-srHSC_pLymph-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1", "Spi1"]].

We used all of those sets J in the second part to identify a multivalued refinement whose asynchronous dynamics would lead to the target reachabilies. In those models, the sets J correspond to the multivalued nodes.

## Identification of multivalued refinement(s)
Run the following command: `python 2.refinement_identification.py -mn ML -p r -m p`. 
