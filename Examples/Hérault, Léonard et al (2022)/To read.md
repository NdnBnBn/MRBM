## Identification of Multivalued Refinements of HSC Aging in Human

**Before running the code:**

* Make sure the files "inputs.py" and "ASYN.bnet" are placed inside the folder named "MRBM".

## Identification of Components for Multivalued Analysis

**Command:**

```python
python 1.multivalued_nodes_identification.py -mn ML -p r
```

**Goal:**

We want to find a multivalued refinement that can capture target reachabilities (possible transitions between states) defined in the "inputs.py" file. These reachabilities can only be observed in the most permissive (m.p.) dynamics of the Boolean model.

First, we need to identify the set of nodes (J) that are sufficient to recover the target reachabilities in the partial J m.p. dynamics. We use the script `1.multivalued_nodes_identification.py` to achieve this.

**Outputs:**

* `FINAL_PARTIAL_SETS_J.txt`: This file lists sets of nodes (J) that partially recover the desired reachabilities.
* `FINAL_SETS_J.txt`: This file contains the set J that fully recovers all the desired reachabilities.
* `TARGET_REACH.txt`: This file specifies the reachability we want to recover in the multivalued refinement.
* `REACH_RES.txt`: This file contains the configuration of the states (initial state and the state we want to reach).

**Results:**

We found only one set J where the partial J m.p. dynamics recovers all the desired reachabilities: ` J = ["Egr1", "Fli1", "Gata1", "Gata2"]`. There are also several other sets J that partially recover the reachabilities (listed below with reachability names separated by "-" and the corresponding set J in square brackets):

* `pME_pEr-preDiff_pEr: [["Fli1"]]`
* `srHSC_pLymph: [["Gata2"], ["Spi1"]]`
* `iHSC_pLymph-srHSC_pLymph: [["Egr1", "Gata2"], ["Egr1", "Spi1"], ["Gata1", "Gata2"], ["Gata2", "Junb"], ["Junb", "Spi1"]]`
* `pME_pEr-preDiff_pEr-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1"]]`
* `pME_pEr-preDiff_pEr-srHSC_pLymph: [["Fli1", "Gata2"], ["Fli1", "Spi1"]]`
* `pME_pEr-preDiff_pEr-iHSC_pLymph-srHSC_pLymph: [["Egr1", "Fli1", "Gata2"], ["Egr1", "Fli1", "Spi1"], ["Fli1", "Gata2", "Junb"], ["Fli1", "Junb", "Spi1"]]`
* `pME_pEr-preDiff_pEr-iHSC_pLymph-srHSC_pLymph-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1", "Gata2"]]`
* `pME_pEr-preDiff_pEr-srHSC_pLymph-qHSC_pNeuMast-qHSC_pEr: [["Fli1", "Gata1", "Spi1"]]`

In the next step, used ` J = ["Egr1", "Fli1", "Gata1", "Gata2"]` to identify a multivalued refinement capable of capturing the target reachabilities, J being the set of multivalued nodes.

## Identification of Multivalued Refinement(s)

**Command:**

```python
python 2.refinement_identification.py -mn ML -p r -m p
```

**Output:**

The script saves the output in a text file named "ML_path_generated_rules.txt".

This file contains regulatory functions that describe the activation conditions of nodes regulated by the multivalued nodes. Those regulatory function were infered by analyzing trajectory that corresponds to a reachabilie of interest (given in the inputs.py file) in the partial J m.p. dynamics with `J = ["Egr1", "Fli1", "Gata1", "Gata2"]`. 

### Interpretation of Refinement Rules

According to the file "ML_path_generated_rules.txt" and the reulatory functions of the original Boolean model several alteration in the regulation of node target by multivalued node can be made. In the following list we define the possible thresholw at which the regulatorion by a multivalued node can occur. If its kept at 1 (like in the Boolean model), it is signaled by "No change":

* Cebpa: No change
* Egr1: Gata2 activates Egr1 at level 2
* **Fli1: Gata1 activated Fli1 at level 2 }**
* Gata1: No change
* Gata2: No change
* Ikzf1: Gata2 activates Ikzf1 at level 2
* **Junb: Egr1 activates Junb at level 2**
* **Klf1: Fli1 inhibit Klf1 at level 2**
* **Spi1: The inhibition by Gata1 and Gata2 occur at level 2**
* Tal1: Gata1 activates Tal1 at level 2
* Zfpm1: No change

### Validation and Minimal Refinement

These suggested changes were tested in a simulation, and they successfully recovered the reachability of interest. We proceded to find the minimal multivalued refinement needed. This involved reducing the changes (setting the threshold of regulation back to 1) one by one and checking if  reachabilities were lost. This iterative process helped us identify the essential modifications required. The final model include only those changes (written in bold in the previous list). 
