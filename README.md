# MRBM

MRBM is a method designed to identify relevent multivalued refinements of a Boolean model (BM). This approach is to be used when the asynchronous dynamics of a BM fail to exhibit a desired reachability property, a property that is, however, satisfied within the most permissive dynamics of the BM. By leveraging the partial most permissive dynamics, MRBM effectively pinpoints nodes that need to be multivalued to recover the desired reachability property. [Read more about MRBM in our paper.](insert link paper)

## Getting Started
The initial step involves defining the reachability property of interest, which could be a specific trajectory toward an attractor or an increase in the basin of attraction size. 

Depending on the property to test you will need to provind and inputs.py file containing three directories:

- mutations: {"node": 0 or 1}
- inits = {"name of state":dict of state} # Set of states to use as inital state to check reachability
- attrs = {"name of attractor":dict of state} # Set of attractors you want to test the reachability towards

inits and attrs dictionary are essential to asses the presence of a specific reachability. When interesting in basin of attraction only the mutations dictionary is necessary. 

It's essential to verify whether the most permissive dynamics exhibit this property, and to ensure it's not observed in the asynchronous dynamics. The first part of the provided notebook does that. If the conditions are met, the MRBM method can then be applied.

MRBM utilizes model checking to ascertain whether a reachability property of interest is oberserved in the partial most permissive dynamics of a BM. 

To generate BM that follows a partial most permissive dynamics we used the model modyfiyer tool provided in biolgm. It generate a BM whose asynchronous dynamics mimics the partial most permissive dynamics. This translation make it so we can use model checking when working with the most permissivr scheme. 

### Prerequisites

The notebook is designed to be fully functional within the Colomoto Docker environment, which provides all the necessary tools and dependencies for MRBM. Access the Colomoto Docker environment [here](https://github.com/colomoto/colomoto-docker).
To generate the partial most permissive dyanamics you will need to install biolqm following this [instructions](http://colomoto.org/biolqm/doc/install.html).
