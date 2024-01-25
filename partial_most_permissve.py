# -*- coding: utf-8 -*-

import subprocess as sp

biolqm = "/home/nadine/Documents/3.Scripts/biolqm.sh"# Biolqm command
model = "/home/nadine/Documents/1.Model&Simulations/2.Leonard_Model/Model/PMP/ASYN.bnet" # Location of the BN model
path = "/home/nadine/Documents/1.Model&Simulations/2.Leonard_Model/Model" # Path of the resulting J mp model


file_path = "/home/nadine/Documents/1.Model&Simulations/2.Leonard_Model/ML_two_pMP_comb.txt"
with open(file_path) as f:
    J = [line.strip() for line in f] # List of sets J¨

# Split names to get nodes
nodes = [n.split("_") for n in J] # Nodes in each set

# Run subprocess for each set of nodes and names
for n, j in zip(nodes, J):
    sp.run([biolqm, model, '  '.join(n), path, j])
