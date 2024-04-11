# MRBM

MRBM is a method designed to identify relevant multivalued refinements of a Boolean model (BM). This approach is to be used when the asynchronous dynamics of a BM fail to exhibit a desired reachability property, a property that is, however, satisfied within the most permissive dynamics of the BM. MRBM effectively pinpoints nodes that need to be multivalued to recover the desired reachability property. Read more about MRBM in our [paper](insert link paper).

## Getting Started

### Prerequisites
Python packages:
  - `pyboolnet`
  - `minibn`
  - `biolqm`
  - `mpbn`

Java toolkit:
  - `Biolqm`

All necessary packages needed can be retrieved using the YAML file mrbm.yml:
  - Installation: `conda env create -f mrbm.yml`
  - Activation: `conda activate mrbm`

### Input files

Depending on the reachability property you are interested in, you will need to provide an `inputs.py` file containing the following Python dictionary:

  - mutations = {"node": 0 or 1}
  - inits = {dict of state} # States to use as initial state to check reachability
  - attrs = {dict of state} # Attractors you want to test the reachability towards
  - reach = {"inits_attrs": [inits, attrs]} # Dict of the reachability to assess

The "inits", "attrs", and "reach" dictionaries are essential to assess the presence of specific reachabilities. They are not needed when looking at the sizes of the basin of attraction (only the "mutations" dictionary is necessary). 

You will also need the BM in a `.bnet` format renamed `ASYN.bnet`.
Both files (the model and the inputs file) need to be in the MRBM directory.

### Identification of multivalued node(s)
Run the code `1.multivalued_nodes_identification.py` using the following arguments:

- mn: model name
- p: define whether you want to check specific reachability (r) or check the basin of attractions (b)
- M: maximal number of m.p. nodes

Examples: 
- `python 1.multivalued_nodes_identification.py -mn model_name -p r -M 5`
- `python 1.multivalued_nodes_identification.py -mn model_name -p b -M 5`

You will obtain the following outputs regardless of the property "p" tested:
- **model_name_FINAL_PARTIAL_SETS_J.txt** : List of sets J that allow to recover part of the basin of attraction sizes |
- **model_name_FINAL_SETS_J.txt** : List of set J that recover all the desired basin of attraction size |

And the following output according to the value p:

| With p = reachability  | With p = basin of attraction |
| ---------------------- | ---------------------------- |
| **model_name_TARGET_MP_BASIN.txt** : List of configuration of attractors and the size of the basin of attraction that are different between the asynchronous and mp dynamics | **model_name_TARGET_REACH.txt** : List of reachabilities that are different between the asynchronous and mp dynamics |
| **model_name_SS.json** : dict of the attractors configuration whose size we want to recover| **model_name_REACH_RES.txt**: dict of the reachabilities we want to recover|
| | **model_name_differences.txt** : reachability result that we expect|

### Identification of multivalued refinement(s)

Run the code `2.refinement_identification.py` using the following arguments: 
- mn: model name
- p: define whether you want to check specific reachability (r) or check the basin of attractions (b)
- m: method to generate multivalued refinement(s), path analysis (p) or test every possible parameterization (c)

Do not change the following parameter if you use the path analysis:
- dj: the default maximal level is 2 (y). If you want to change it (n) provide new mj value (nm) 
- nm: dictionary of the new maximal value for each node {'mv node': mj_value,...}

Examples: 
- `python 2.refinement_identification.py -mn model_name -p r -m p`
- `python 2.refinement_identification.py -mn model_name -p b -m c -dj n -nm '{"G1":3}'`

You will obtain the following outputs depending on the method used for the identification of multivalued refinements:
- If m = p, you will obtain a text file with possible rules of the nodes regulated by multivalued component. The level of multivalued node is indicated by a number after a "-". Example: G1-1 means component G1 at level 1.
- If m = c, you will obtain a text file with all multivalued models satisfying the property you are verifying. The models are in `.bnet` format.
