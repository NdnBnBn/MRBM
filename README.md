# MRBM

MRBM is a method designed to identify relevent multivalued refinements of a Boolean model (BM). This approach is to be used when the asynchronous dynamics of a BM fail to exhibit a desired reachability property, a property that is, however, satisfied within the most permissive dynamics of the BM. MRBM effectively pinpoints nodes that need to be multivalued to recover the desired reachability property. Read more about MRBM in our [paper](insert link paper).

## Getting Started

### Prerequisites
Python packages:
  - `pyboolnet`
  - `minibn`
  - `biolqm`
  - `mpbn`

Java toolkit:
  - `Biolqm`

All necessary package needed can be retrived using the yml file mrbm.yml:
  - Installation: `conda env create -f mrbm.yml`
  - Activation: `conda activate mrbm`

### Inputs files

Depending on the  reachability property you are interested in you will need to provind and inputs.py file containing the following python dict:

  - mutations: {"node": 0 or 1}
  - inits = {dict of state} # States to use as inital state to check reachability
  - attrs = {dict of state} # Attractors you want to test the reachability towards
  - reach = {"inits_attrs": [inits, attrs]} # Dict of the reachability to asses

The inits, attrs, and reach dictionaries are essential to asses the presence of a specific reachability. They are not needed when looking at the sizes of the basin of attraction (only the mutations dictionary is necessary). 

You will also need the BM in a `.bnet` format.
Both files need to be in the MRBM dictory.

### Identification of multivalued node(s)
Run the code `1.multivalued_nodes_identification.py` using the following arguments:

    - mn, --model_name     enter model_name
    - p {b,r}, --property {b,r}     define wheather you want check sepecific reachability (r) or check the basin of attractions (b)                   
    - M MAX, --MAX MAX     maximal number of m.p. nodes


### Identification of multivalued refinement(s)

Run the code `2.refinement_identification.py` using the following arguments: 

    - mn, --model_name      enter model_name
    - p {b,r}, --property {b,r}     define wheather you want check sepecific reachability (r) or check the basin of attractions (b)                  
    - m {p,c}, --method {p,c}       method to generate multivalued refinement(s), path analysis (p) or test every possible parameterization (c)                   
    - dj {y,n}, --default_mj {y,n} (y)      the default maximal level if 2. if not provide new mj value (-nm)                   
    - nm, --new_mj      dictionnary of the new maximal value for each node {'mv nod':'mj value',...}`
