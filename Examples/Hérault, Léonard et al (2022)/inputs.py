#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Attractors

mutations = {}

# Transient states
zeros = {'Bclaf1': 0,'CDK46CycD': 0,'CIPKIP': 0,'Cebpa': 0,'Egr1': 0,'Fli1': 0,'Gata1': 0,'Gata2': 0,'Ikzf1': 0,'Junb': 0,'Klf1': 0,'Myc': 0,'Spi1': 0,'Tal1': 0,'Zfpm1': 0}
pME = zeros.copy()
for k, v in list(pME.items()): 
    if k.startswith("Junb"):
        pME[k] = 1 
    if k.startswith("Bclaf1"):
        pME[k] = 1
    if k.startswith("Myc"):
        pME[k] = 1
    if k.startswith("Tal1"):
        del pME[k]
    if k.startswith("Ikzf1"):
        del pME[k]
    if k.startswith("Zfpm1"):
        del pME[k]

preDiff = zeros.copy()
for k, v in list(preDiff.items()): 
    if k.startswith("Spi1"):
        preDiff[k] = 1 
    if k.startswith("Bclaf1"):
        preDiff[k] = 1
    if k.startswith("Myc"):
        preDiff[k] = 1
    if k.startswith("Tal1"):
        del preDiff[k]
    if k.startswith("Ikzf1"):
        del preDiff[k]
    if k.startswith("Zfpm1"):
        del preDiff[k]

iHSC = zeros.copy()
for k, v in list(iHSC.items()): 
    if k.startswith("Fli1"):
        iHSC[k] = 1 
    if k.startswith("Bclaf1"):
        iHSC[k] = 1
    if k.startswith("Gata2"):
        iHSC[k] = 1
    if k.startswith("Tal1"):
        del iHSC[k]
    if k.startswith("Zfpm1"):
        del iHSC[k]

srHSC = zeros.copy()
for k, v in list(srHSC.items()): 
    if k.startswith("Egr1"):
        srHSC[k] = 1 
    if k.startswith("Bclaf1"):
        srHSC[k] = 1
    if k.startswith("Fli1"):
        srHSC[k] = 1
    if k.startswith("CDK46CycD"):
        srHSC[k] = 1
    if k.startswith("Tal1"):
        del srHSC[k]
    if k.startswith("Ikzf1"):
        del srHSC[k]
    if k.startswith("Zfpm1"):
        del srHSC[k]

qHSC = zeros.copy()
for k, v in list(qHSC.items()): 
    if k.startswith("Egr1"):
        qHSC[k] = 1 
    if k.startswith("Junb"):
        qHSC[k] = 1
    if k.startswith("Fli1"):
        qHSC[k] = 1
    if k.startswith("Myc"):
        qHSC[k] = 1
    if k.startswith("Gata2"):
        qHSC[k] = 1
    if k.startswith("Tal1"):
        qHSC[k] = 1
    if k.startswith("CDK46CycD"):
        qHSC[k] = 1
    if k.startswith("CIPKIP"):
        qHSC[k] = 1
    if k.startswith("Zfpm1"):
        del qHSC[k]
        
# Attractors

pLymph = {'Bclaf1': 0,'CDK46CycD': 0,'CIPKIP': 0,'Cebpa': 0,'Egr1': 0,'Fli1': 0,'Gata1': 0,'Gata2': 1,'Ikzf1': 1,'Junb': 0,'Klf1': 0,'Myc': 0,'Spi1': 1,'Tal1': 0,'Zfpm1': 0}
pNeuMast = {'Bclaf1': 0,'CDK46CycD': 0,'CIPKIP': 0,'Cebpa': 1,'Egr1': 0,'Fli1': 0,'Gata1': 0,'Gata2': 0,'Ikzf1': 0,'Junb': 0,'Klf1': 0,'Myc': 0,'Spi1': 1,'Tal1': 0,'Zfpm1': 0}
pMk = {'Bclaf1': 0,'CDK46CycD': 0,'CIPKIP': 0,'Cebpa': 0,'Egr1': 0,'Fli1': 1,'Gata1': 1,'Gata2': 0,'Ikzf1': 0,'Junb': 0,'Klf1': 0,'Myc': 0,'Spi1': 0,'Tal1': 1,'Zfpm1': 1}
pEr = {'Bclaf1': 0,'CDK46CycD': 0,'CIPKIP': 0,'Cebpa': 0,'Egr1': 0,'Fli1': 0,'Gata1': 1,'Gata2': 0,'Ikzf1': 0,'Junb': 0,'Klf1': 1,'Myc': 0,'Spi1': 0,'Tal1': 1,'Zfpm1': 1}

inits = {"pME":pME,
         "preDiff":preDiff,
         "iHSC":iHSC,
         "srHSC":srHSC,
         "qHSC":qHSC}
         
reach = {"pME_pLymph": [pME, pLymph],
         "pME_pNeuMast": [pME, pNeuMast],
         "pME_pMk": [pME, pMk],
         "pME_pEr": [pME, pEr],
         
         "preDiff_pLymph": [preDiff, pLymph],
         "preDiff_pNeuMast": [preDiff, pNeuMast],
         "preDiff_pMk": [preDiff, pMk],
         "preDiff_pEr": [preDiff, pEr],
         
         "iHSC_pLymph": [iHSC, pLymph],
         "iHSC_pNeuMast": [iHSC, pNeuMast],
         "iHSC_pMk": [iHSC, pMk],
         "iHSC_pEr": [iHSC, pEr],
         
         "srHSC_pLymph": [srHSC, pLymph],
         "srHSC_pNeuMast": [srHSC, pNeuMast],
         "srHSC_pMk": [srHSC, pMk],
         "srHSC_pEr": [srHSC, pEr],
         
         "qHSC_pLymph": [qHSC, pLymph],
         "qHSC_pNeuMast": [qHSC, pNeuMast],
         "qHSC_pMk": [qHSC, pMk],
         "qHSC_pEr": [qHSC, pEr]}
