#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:00:15 2024

@author: nadine
"""

import os
import csv
import json
import argparse
import biolqm
from pyboolnet import prime_implicants
from pyboolnet import file_exchange
from pyboolnet.state_transition_graphs import best_first_reachability
from pyboolnet.attractors import read_attractors_json
from pyboolnet.state_space import size_state_space
import mpbn
import inputs as ip
from mrbm import basin
from mrbm import reachability
from mrbm import mv_models_initialisation
from mrbm import mv_rules_generator
from mrbm import mv_models_rules_combinations
from mrbm import mv_models
from mrbm import bool_to_jmp
from mrbm import path_generated_rules
from mrbm import most_similar_lists
from mrbm import remove_files_except

parser = argparse.ArgumentParser()
parser.add_argument("-mn", "--model_name",
                    help="enter model_name",
                    type=str)
parser.add_argument("-p", "--property",
                    help="define wheather you want check sepecific reachability (r) or check the basin of attractions (b)",
                    type=str,
                    choices=["b", "r"])
parser.add_argument("-m", "--method",
                    help="method to generate multivalued refinement(s), path analysis (p) or test every possible parameterization (c)",
                    type=str,
                    choices=["p", "c"])
parser.add_argument("-dj", "--default_mj",
                    help="(y) the default maximal level if 2. if not provide new mj value (-nm)",
                    type=str,
                    default= "y",
                    choices=["y", "n"])

parser.add_argument("-nm", "--new_mj",
                    help="dictionnary of the new maximal value for each node {'mv nod':'mj value',...}",
                    type=json.loads)

parser.add_argument("-j", "--setj",
                    help="path to the setj to test",
                    type=str)

args = parser.parse_args()



CDIR = os.getcwd()
JMP_DIR = CDIR + "/JMP_Models"
MV_DIR = CDIR + "/MV_Models"
temp = CDIR + "/temp"
if not os.path.exists(MV_DIR):
    os.mkdir(MV_DIR)
if not os.path.exists(temp):
    os.mkdir(temp)

#args.model_name = "ML"
#args.property = "r"
#args.method = "p"
#args.default_mj = "y"
#args.setj = f"{args.model_name}_FINAL_SETS_J.txt"


# Loading results from the set J identification
if os.path.exists(f"{args.model_name}_SS.json"):
    SS = read_attractors_json(f"{args.model_name}_SS.json")

if os.path.exists(f"{args.model_name}_TARGET_MP_BASIN.txt"):
    with open(f"{args.model_name}_TARGET_MP_BASIN.txt", "r") as file:
        TARGET_MP_BASIN = json.load(file)

if os.path.exists(f"{args.model_name}_TARGET_REACH.txt"):
    with open(f"{args.model_name}_TARGET_REACH.txt", "r") as file:
        TARGET_REACH = json.load(file)

if os.path.exists(f"{args.model_name}_REACH_RES.txt"):
    with open(f"{args.model_name}_REACH_RES.txt", "r") as file:
        REACH_RES = json.load(file)

if os.path.exists(args.setj):
    with open(args.setj, "r") as file:
        FINAL_SETS_J = json.load(file)

if type(FINAL_SETS_J) == dict:
    KEY = list(FINAL_SETS_J.keys())[0].split('-')
    FINAL_SETS_J = list(*FINAL_SETS_J.values())
    print(KEY)
    if args.property == "b":
        SS = [s for s in SS if s["state"]["str"] in KEY]
        TARGET_MP_BASIN = [item for item in TARGET_MP_BASIN if item[0] in KEY]
        print(SS)
    elif args.property == "r":
        REACH_RES = {key: value for key, value in REACH_RES.items() if key in KEY}
        TARGET_REACH = {key: value for key, value in TARGET_REACH.items() if key in KEY}
#if os.path.exists(f"{args.model_name}_FINAL_PARTIAL_SETS_J.txt"):
#    with open(f"{args.model_name}_FINAL_PARTIAL_SETS_J.txt", "r") as file:
#        FINAL_PARTIAL_SETS_J = json.load(file)

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
# Identification of multivalued refinement asynchronous dynamics satisfying P
#==============================================================================
SIZE = size_state_space(PRIMES_ASYN)

if args.method == "p": # Path analysis
    MEM = 10000
    NPATH = 2
    for SETJ in FINAL_SETS_J:
        JMP_NAME = '_'.join(SETJ)
        PRIMES = file_exchange.bnet2primes(JMP_DIR+"/"+JMP_NAME+"_mp.bnet")
        TRAJ = []
        for key in REACH_RES.keys():
            TRAJ.append([key, best_first_reachability(PRIMES,
                                                      bool_to_jmp(ip.reach[key][0], JMP_NAME),
                                                      bool_to_jmp(ip.reach[key][1], JMP_NAME),
                                                      memory=MEM)])
        RULES = path_generated_rules(PRIMES_ASYN, SETJ, PRIMES, JMP_NAME, TRAJ)
        if RULES:
            with open(args.model_name+"_path_generated_rules.txt", 'w') as file:
                for key, value in RULES.items():
                    file.write(f"{key}: {value}\n")
        else:
            if not TRAJ:
                print("No detected trajectory")
            if TRAJ:
                print("The path is not informative")

else: # Test every possible multivaluation (very long + many solutions)
    FINAL_MV = {}
    IDX = 0
    for SETJ in FINAL_SETS_J:
        MV_NAME = '_'.join(SETJ)
        if args.default_mj == "y":
            mj_list = [2] * len(SETJ)
        elif args.default_mj == "n" : mj_list = [args.new_mj.get(value, 2) for value in SETJ]

        if args.new_mj:
            newmv = []
            for key, value in args.new_mj.items():
                newmv.append(f"{key}{value}")
            newmv = "_".join(newmv)
            path = f'MV({MV_NAME})_{newmv}_RULES.csv'
        else: path = f'MV({MV_NAME})_RULES.csv'

        if not os.path.isfile(path):
            MV_INIT = mv_models_initialisation(SETJ, BNA, mj_list)
            MV_RULES, ALL_RULES = mv_rules_generator(MV_INIT[MV_NAME], MV_NAME, mj_list)
            ALL_MV_RULES = mv_models_rules_combinations(MV_RULES, ALL_RULES)

            with open(path, 'w', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                for row in ALL_MV_RULES:
                    writer.writerow([row])
        else:
            ALL_MV_RULES = []
            with open(path, 'r', newline='') as f:
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    tuples = eval(row[0])
                    ALL_MV_RULES.append(tuples)

        for a in ALL_MV_RULES:
            MV = mv_models(a)
            MV_LQM = MV.to_biolqm()
            MV_PRIMES = biolqm.to_pyboolnet(MV_LQM)
            for g, v in ip.mutations.items():
                if {g}.issubset(SETJ):
                    for mj in mj_list:
                        prime_implicants.create_constants(MV_PRIMES,
                                                          {f"{g}_b{i}": v for i in range(1, mj+1)})
                else:
                    prime_implicants.create_constants(MV_PRIMES, {g:v})

            if args.property == "b":
                MV_BOA = basin(MV_NAME, MV_PRIMES, SS, "mv", SIZE, mj_list)
                print("MV "+str(IDX))
                IDX += 1
                if MV_BOA == TARGET_MP_BASIN:
                    FINAL_MV[f'/MV({MV_NAME})_MODEL{IDX}.bnet'] = []
                    biolqm.save(MV_LQM, temp+f'/MV({MV_NAME})_MODEL{IDX}.bnet')
                    FINAL_MV[f'/MV({MV_NAME})_MODEL{IDX}.bnet'].append(MV)

            elif args.property == "r":
                MV_REACH = reachability(MV_NAME, TARGET_REACH, MV_PRIMES, "mv", mj_list)
                print("MV "+str(IDX))
                IDX += 1
                if MV_REACH == REACH_RES:
                    FINAL_MV[f'/MV({MV_NAME})_MODEL{IDX}.bnet'] = []
                    biolqm.save(MV_LQM, temp+f'/MV({MV_NAME})_MODEL{IDX}.bnet')
                    FINAL_MV[f'/MV({MV_NAME})_MODEL{IDX}.bnet'].append(MV)



    if len(FINAL_MV):
        most_similar = most_similar_lists(BNA,FINAL_MV)
        remove_files_except(most_similar, temp, MV_DIR)


#mv = biolqm.load("MV3.zginml")
#MV_NAME = '_'.join(('SCR', 'SHR','MGP'))
#MV_PRIMES = biolqm.to_pyboolnet(mv)
#if {g}.issubset(SETJ):
#    for mj in mj_list:
#        prime_implicants.create_constants(MV_PRIMES,
#                                          {f"{g}_b{i}": v for i in range(1, mj + 1)})
#else:
#    prime_implicants.create_constants(MV_PRIMES, {g:v})
#MV_BOA = basin(MV_NAME, MV_PRIMES, SS, "mv", SIZE, [3,2,2])
#MV_BOA
