# MRBM

MRBM is a method designed to identify relevent multivalued refinements of a Boolean model (BM). This approach is to be used when the asynchronous dynamics of a BM fail to exhibit a desired reachability property, a property that is, however, satisfied within the most permissive dynamics of the BM. MRBM effectively pinpoints nodes that need to be multivalued to recover the desired reachability property. Read more about MRBM in our [paper](insert link paper).

## Getting Started

Depending on the  reachability property you are interested in you will need to provind and inputs.py file containing the following directories:

  - mutations: {"node": 0 or 1}
  - inits = {dict of state} # States to use as inital state to check reachability
  - attrs = {dict of state} # Attractors you want to test the reachability towards
  - reach = {"inits_attrs": [inits, attrs]} # Dict of the reachability to asses

The inits, attrs, and reach dictionaries are essential to asses the presence of a specific reachability. They are not needed when looking at the sizes of the basin of attraction (only the mutations dictionary is necessary). 

### Prerequisites
Python packages:
  - pyboolnet
  - minibn
  - biolqm
  - mpbn

Java package:
  - Biolqm
All necessary package needed can be retrived using the yml file mrbm.yml:
  - Installation: conda env create -f mrbm.yml
  - Activation: `conda activate mrbm`
