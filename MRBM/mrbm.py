#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Feb 20 13:05:25 2024

@author: Nadine Ben Boina
"""

from itertools import product
import copy
from pyboolnet.model_checking import model_checking
from pyboolnet.temporal_logic import subspace2proposition
from colomoto import minibn
from pyboolnet import prime_implicants
from pyboolnet.prime_implicants import find_predecessors
from pyboolnet.state_space import state2dict
from pyboolnet.boolean_logic import minimize_espresso
import os

def mv_models_initialisation(setJ, bna, mj_list):
    """ MV nodes in the format node:mj <- Associated rules. Simple change in the syntax of anymv node
    """
    pre_mv = {}
    new_model = bna.copy()
    if len(setJ) > 1:
        for i, mj in zip(setJ, mj_list):
            new_model[i + f":{mj}"] = new_model[i]
            del new_model[i]
    else:
        for mj in mj_list:
            new_model[setJ[0] + f":{mj}"] = new_model[setJ[0]]
            del new_model[setJ[0]]
    pre_mv['_'.join(setJ)] = new_model
    return pre_mv

def mv_rules_generator(mv_model, model_name, mj_list):
    """Given the model given by the previous function, for any targets of the mv nodes gives any
    possible rules with the threshold of regulation being at 1 or up to mj
    """
    mv_rules = {}
    all_rules = []
    mv_nodes = model_name.split("_")

    for i, rule in mv_model.items():
        rule_str = str(rule)
        mv_temp = []
        n = 0

        for j, mj in zip(mv_nodes, mj_list):
            if j in rule_str:
                mv_rules[i] = []
                mv_temp.append([j])
                mv_temp[n].extend([(f"{j}:{k}") for k in range(2, mj + 1)])
                n+=1

        if len(mv_temp) > 1:
            mv_rulei = list(product(*mv_temp))
        else:
            mv_rulei = mv_temp

        if len(mv_temp) > 1:
            mv_rulei = list(product(*mv_temp))
        else:
            mv_rulei = mv_temp

        if len(mv_rulei) > 0:
            if len(mv_rulei) > 1:
                for m in mv_rulei:
                    new_rule = rule_str.replace(m[0].split(':')[0], m[0])
                    for l in range(1, len(m)):
                        new_rule = new_rule.replace(m[l].split(':')[0], m[l])
                    mv_rules[i].append((i, new_rule))
            else:
                for m in mv_rulei:
                    for mn in m:
                        new_rule = rule_str.replace(mn.split(':')[0], mn)
                        mv_rules[i].append((i, new_rule))
        else: all_rules.append((i, rule_str))
    return mv_rules, all_rules

def mv_models_rules_combinations(mv_rules, all_rules):
    """Give all the possible combinations of mv_rules +  Add non changing rules
    """
    rules = list(set(product(*mv_rules.values())))
    if all_rules:
        rules = [combination + tuple(all_rules) for combination in rules]

    return rules

def mv_models(rules):
    """Create mv model
    """
    mv = minibn.MultiValuedNetwork()
    for r in rules:
        if isinstance(r, list):
            for a, f in r:
                mv.append(a, f)
        else:
            a, f = r
            mv.append(a, f)
    return mv # With the rules create a mv model in the minibn format

def bool_to_jmp(state, node):
    """ This function translate any Boolean state (in dict format) in a most
    permissive state with m being a list of most permissve nodes
    """
    states = copy.deepcopy(state)
    for k in node.split("_"):
        if k in states:
            v = states[k]
            for suffix in ['_a', '_b', '_c']:
                states[k + suffix] = v
            del states[k]
    return states

def bool_to_mv(state, node, mj_list):
    """ This function translate any Boolean state (in dict format) in a most
    multivalued state with m being a list of multivalued permissve nodes
    """
    states = copy.deepcopy(state)
    for k, mj in zip(node.split("_"), mj_list):
        if k in states:
            v = states[k]
            for suffix in [f"_b{i}" for i in range(1, mj + 1)]:
                states[k + suffix] = v
            del states[k]
    return states

def jmp_to_mv(state, node, mj):
    """ This function translate any jmp state (in dict format) in a mv with given a list of most
    permissve nodes and a maximum lelvel of activity mj
    """
    states = copy.deepcopy(state)
    for k in list(states.keys()):
        if k.endswith("_c"):
            node = k[:-2]
            a, b, c = (states[node + "_a"], states[node + "_b"], states[node + "_c"])
            code_map = {(0, 0, 0): 0,
                        (1, 1, 1): mj,
                        (1, 0, 0): 1,
                        (1, 1, 0): "?",
                        (0, 1, 1): 1,
                        (0, 0, 1): 1,
                        (1, 0, 1): 1,
                        (0, 1, 0): "?"}

            states[node] = code_map.get((a, b, c), states.get(node))

            # Delete the old keys
            del states[node + "_a"]
            del states[node + "_b"]
            del states[node + "_c"]

    return states

def basin(name, model, attractors, lm, size, mj_list = []):
    """ This function computes the basin of attraction of a logical model in the asynchronous
    dynamics. The input is the model name (model), the model in primes format (primes), the set of
    attractors of the model and if the model is Boolean, multivalued or partial most permissive
    (lm = bm, mv or mp).
    """
    if lm == "mp":
        mpn = [k[:-2] for k, _ in model.items() if k.endswith("_c")]
        if mpn:
            clause = [f"(({n}_a&{n}_b&{n}_c) | (!{n}_a&!{n}_b&!{n}_c))" for n in mpn]
            init = f"INIT {' & '.join(clause)}"
    elif lm == "mv":
        clauses = []
        for node, mj in zip(name.split("_"), mj_list):
                mv_list = [f"{node}_b{i}" for i in range(1, mj + 1)]
                clause = f"({'&'.join(mv_list)} | {'&'.join(['!' + mv for mv in mv_list])})"
                clauses.append(clause)
        init = f"INIT {' & '.join(clauses)}"
    else:
        init = "INIT TRUE"

    boa = []
    for i in range(len(attractors)):
        if lm == "mp":
            attr = bool_to_jmp(attractors[i]["state"]["dict"], name)
        elif lm == "mv":
            attr = bool_to_mv(attractors[i]["state"]["dict"], name, mj_list)
        else:
            attr = attractors[i]["state"]["dict"]
        specification = f"CTLSPEC EF({subspace2proposition(model, attr)})"
        _, accepting_states = model_checking(model,
                                             "asynchronous",
                                             init,
                                             specification,
                                             enable_accepting_states = True)
        boa.append([attractors[i]["state"]["str"],
                    accepting_states["INITACCEPTING_SIZE"]/size*100])
    return boa

def mp_basin(attractors, MBN, size):
    boa = []
    for i in range(len(attractors)):
        states = list(MBN.reachable_from(attractors[i]["state"]["dict"], reversed= True))
        s = attractors[i]["state"]["str"]
        boa.append([s, len(states)/size*100])
    return boa

def reachability(name, reach, model, lm):
    """
    Assess the existence of a trajectory from an initial state to a fixed point.

    Args:
    - name: Name of the model.
    - reach: Dictionary containing target states and associated state pairs.
    - model: Model in primes format.
    - lm: Type of the model (bm, mv, or mp).

    Returns:
    - answer: Dictionary containing assessment results.
    """
    init = {}
    for key, value in reach.items():
        if name == "ASYN":
            init[key] = f"INIT {subspace2proposition(model, value[0])}"
        elif lm == "mp":
            init[key] = f"INIT {subspace2proposition(model, bool_to_jmp(value[0], name))}"
        elif lm == "mv":
            init[key] = f"INIT {subspace2proposition(model, bool_to_mv(value[0], name))}"

    answer = {}
    for key, value in reach.items():
        answer[key] = []
        if name == "ASYN":
            attr_state = value[1]
        elif lm == "mp":
            attr_state = bool_to_jmp(value[1], name)
        elif lm == "mv":
            attr_state = bool_to_mv(value[1], name)

        specification = f"CTLSPEC EF({subspace2proposition(model, attr_state)})"
        res = model_checking(model, "asynchronous", init[key], specification)
        answer[key].append(res)
    return answer

def mp_reach(reach, MBN):
    answer = {}
    for key, value in reach.items():
        answer[key] = []
        res = MBN.reachability(value[0], value[1])
        answer[key].append(res)
    return answer

def path_generated_rules(model_asyn, set_j, model_pmp, model_name, trajectories):
    NODES = list(model_asyn)
    TARGETS = prime_implicants.find_successors(model_asyn, set_j)
    DICT = {T[0]: [jmp_to_mv(state2dict(model_pmp, state), model_name, 2) for state in T[1]] for T in trajectories}

    NEG = {T: [] for T in TARGETS}
    POS = {T: [] for T in TARGETS}

    for T in TARGETS:
        for D in DICT:
            for i in range(1, len(DICT[D])):
                current_state = DICT[D][i]
                previous_state = DICT[D][i - 1]

                if previous_state[T] != current_state[T]:
                    copy = previous_state.copy()
                    for N in NODES:
                        if N not in find_predecessors(model_asyn, [T]):
                            del copy[N]
                    rule = str(copy).replace(",", " and").strip("{}\"")
                    if current_state[T] == 0:
                        NEG[T].append(rule)
                    else:
                        POS[T].append(rule)

    for T in TARGETS:
        for ruleset in (NEG[T], POS[T]):
            for i, rule in enumerate(ruleset):
                for N in NODES:
                    rule = rule.replace(f"'{N}': 1", N).replace(f"'{N}': 0", "!" + N).replace(f"'{N}': 2", N + "_2").replace("and", "&")
                ruleset[i] = rule

    RULES = {}
    for T in TARGETS:
        neg_rule = " | ".join(NEG[T])
        pos_rule = " | ".join(POS[T])

        if neg_rule and pos_rule:
            RULES[T] = f"({pos_rule}) & !({neg_rule})"
        else:
            RULES[T] = pos_rule or f"!({neg_rule})"
        RULES[T] = minimize_espresso(RULES[T], merge=True, equiv=True, exact=True, reduce=True)

    return RULES

def minimize_dict(data):
    minimized_data = {}
    for key, values in data.items():
        min_size = min(len(val) for val in values)
        minimized_values = [val for val in values if len(val) == min_size]
        minimized_data[key] = minimized_values
    return minimized_data

def empty_folder_except(folder_path, files_to_keep):
    all_files = os.listdir(folder_path)
    for file_name in all_files:
        if file_name not in files_to_keep:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
