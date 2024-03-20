#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Feb 20 13:05:25 2024

@author: nadine
"""

import os
import subprocess as sp
from itertools import combinations
import biolqm
from pyboolnet import prime_implicants
from pyboolnet.attractors import compute_attractors, write_attractors_json
from pyboolnet import file_exchange
from pyboolnet.state_space import size_state_space
import mpbn
import inputs as ip
from functions import basin
from functions import mp_basin
from functions import reachability
from functions import mp_reach
from functions import empty_folder_except
from functions import minimize_dict
import json

CDIR = os.getcwd()
MODEL_NAME = input("Enter the name of the model: \n") # Name of the model

#==============================================================================
# Loading the Boolean model with possible mutation stored in an inputs.py file
#==============================================================================
PRIMES_ASYN = file_exchange.bnet2primes(CDIR+"/ASYN.bnet")
LQM = biolqm.load(CDIR+"/ASYN.bnet")
BNA = biolqm.to_minibn(LQM)
MBN = mpbn.MPBooleanNetwork(BNA) # Most permissive model

# Mutation in the model
for g, v in ip.mutations.items():
    prime_implicants.create_constants(PRIMES_ASYN, {g:v})
    MBN[g] = v

#==============================================================================
# Computing the attractors: stable states and cyclic.
#==============================================================================
AT_SYN = compute_attractors(PRIMES_ASYN, "asynchronous")
AT_MP = list(MBN.attractors())
STABLE_STATES = {}
CYCLIC_ATTRACTORS = {}
STABLE_STATES["ASYN"] = {i: attractor for i, attractor in enumerate(AT_SYN["attractors"]) if not attractor["is_cyclic"]}
CYCLIC_ATTRACTORS["ASYN"] = {i: attractor for i, attractor in enumerate(AT_SYN["attractors"]) if attractor["is_cyclic"]}
STABLE_STATES["MP"] = {i: attractor for i, attractor in enumerate(AT_MP) if "*" not in attractor.values()}
CYCLIC_ATTRACTORS["MP"] = {i: attractor for i, attractor in enumerate(AT_MP) if "*" in attractor.values()}


if not CYCLIC_ATTRACTORS["ASYN"] and not CYCLIC_ATTRACTORS["MP"]:
    print("There are no cyclic attractors")

#==============================================================================
# Assessing reachability property P in the asynchronous and mp dynamics
#==============================================================================

PROPERTY = input("Enter the property to check between 'basin' and 'reachability': \n")

if PROPERTY == "basin":
    SIZE = size_state_space(PRIMES_ASYN)
    ASYN_BOA = basin("ASYN", PRIMES_ASYN, STABLE_STATES["ASYN"], "bm", SIZE)
    MP_BOA = mp_basin(STABLE_STATES["ASYN"], MBN, SIZE)
    if ASYN_BOA != MP_BOA:
        ASYN_set = set(tuple(row) for row in ASYN_BOA)
        MP_set = set(tuple(row) for row in MP_BOA)
        TARGET_MP_BASIN = [row for row in MP_BOA if tuple(row) not in ASYN_set]
        SS = []
        TARG_ATTR = [sublist[0] for sublist in TARGET_MP_BASIN]
        for i in range(len(STABLE_STATES["ASYN"])):
            if STABLE_STATES["ASYN"][i]["state"]["str"] in TARG_ATTR:
                SS.append(STABLE_STATES["ASYN"][i])
        write_attractors_json(SS, f"{MODEL_NAME}_SS.json")
        with open(f"{MODEL_NAME}_TARGET_MP_BASIN.txt", "w") as file:
            json.dump(TARGET_MP_BASIN, file)
        NEXT = "Keep going"

if PROPERTY == "reachability":
    ASYN_REACH = reachability("ASYN", ip.reach, PRIMES_ASYN, "bm")
    MP_REACH = mp_reach(ip.reach, MBN)
    differences = {}
    REACH_RES = {}
    for key in ASYN_REACH.keys():
        if ASYN_REACH[key] != MP_REACH[key]:
            differences[key] = ASYN_REACH[key]
            REACH_RES[key] = MP_REACH[key]
            TARGET_REACH = {key: ip.reach[key] for key in differences.keys()}
            NEXT = "Keep going"

    with open(f"{MODEL_NAME}_differences.txt", "w") as file:
        json.dump(differences, file)
    with open(f"{MODEL_NAME}_REACH_RES.txt", "w") as file:
        json.dump(REACH_RES, file)
    with open(f"{MODEL_NAME}_TARGET_REACH.txt", "w") as file:
        json.dump(TARGET_REACH, file)

#==============================================================================
# Identification of a set J for wich the patial Jm.p. dynamics satisfies P
#==============================================================================
SELF_NO = [i for i in PRIMES_ASYN if f"!{i}" in str(BNA[i])]
OUTPUTS = prime_implicants.find_outputs(PRIMES_ASYN)
ADMISSIBLE_NODE = [item for item in PRIMES_ASYN if item not in OUTPUTS and item not in SELF_NO]

NEW_MAX = input("Do you want to test more than 5 mp node? (y/n): \n")
if NEW_MAX == "y":
    NEW = input("Give a new value: \n")
    MAX = min(len(BNA), int(NEW))
else: MAX = min(len(BNA), 5)

FINAL_SETS_J = []
PARTIAL_SETS_J = {}
IDX = 0
if NEXT:
    CMD_BIOLQM = "/home/nadine/Documents/3.Scripts/biolqm.sh"
    JMP_DIR = CDIR + "/JMP_Models"
    if not os.path.exists(JMP_DIR):
        os.mkdir(JMP_DIR)
    for m in range(1, MAX+1):
        SETS_J = list(combinations(ADMISSIBLE_NODE, m))
        for j in SETS_J:
            JMP_NAME = '_'.join(j)
            sp.run([CMD_BIOLQM, CDIR+"/ASYN.bnet", ' '.join(j), JMP_DIR, JMP_NAME], check=True)
            PATH = JMP_DIR + "/" + JMP_NAME + "_mp.bnet"
            JMP_MODEL = file_exchange.bnet2primes(PATH)
            for g, v in ip.mutations.items():
                if {g}.issubset(j):
                    prime_implicants.create_constants(JMP_MODEL, {g+"_a":v, g+"_b":v, g+"_c":v})
                else:
                    prime_implicants.create_constants(JMP_MODEL, {g:v})

            if PROPERTY == "basin":
                JMP_BOA = basin(JMP_NAME, JMP_MODEL, SS, "mp", SIZE)
                print("PMP "+str(IDX))
                IDX += 1
                if any(item in JMP_BOA for item in TARGET_MP_BASIN):
                    IDC = [item1 for item1 in TARGET_MP_BASIN if any(item1[1] == item2[1] for item2 in JMP_BOA)]
                    if len(IDC) == len(TARGET_MP_BASIN):
                        FINAL_SETS_J.append(j)
                    else:
                        N = [item[0] for item in IDC]
                        N = "_".join(N)
                        if PARTIAL_SETS_J.get(N) == None:
                            PARTIAL_SETS_J[N] = []
                            PARTIAL_SETS_J[N].append(j)
                        else:
                            PARTIAL_SETS_J[N].append(j)
                else: os.remove(PATH)

            if PROPERTY == "reachability":
                JMP_REACH = reachability(JMP_NAME, TARGET_REACH, JMP_MODEL, "mp")
                print("PMP "+str(IDX))
                IDX += 1
                if any(item in JMP_REACH.items() for item in REACH_RES.items()):
                    IDC = [(key, value) for key, value in REACH_RES.items() if JMP_REACH.get(key) == value]
                    if len(IDC) == len(REACH_RES):
                        FINAL_SETS_J.append(j)
                    else:
                        N = [item[0] for item in IDC]
                        N = "_".join(N)
                        if PARTIAL_SETS_J.get(N) == None:
                            PARTIAL_SETS_J[N] = []
                            PARTIAL_SETS_J[N].append(j)
                        else:
                            PARTIAL_SETS_J[N].append(j)
                else: os.remove(PATH)

        if len(FINAL_SETS_J) > 0:
            FINAL_PARTIAL_SETS_J = minimize_dict(PARTIAL_SETS_J)
            with open(f"{MODEL_NAME}_FINAL_SETS_J.txt", "w") as file:
                json.dump(FINAL_SETS_J, file)
            with open(f"{MODEL_NAME}_FINAL_PARTIAL_SETS_J.txt", "w") as file:
                json.dump(FINAL_PARTIAL_SETS_J, file)
            break

ALL_SETJS = []
for key, values in FINAL_PARTIAL_SETS_J.items():
    ALL_SETJS.extend(values)
for J in FINAL_SETS_J:
    ALL_SETJS.append(J)

MODEL_TO_KEEP = []
for SET in ALL_SETJS:
    NAME = "_".join(SET)
    MODEL_TO_KEEP.append(f"{NAME}_mp.bnet")
empty_folder_except(JMP_DIR, MODEL_TO_KEEP)
