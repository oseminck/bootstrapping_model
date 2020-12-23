#!/usr/bin/env python # -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import argparse

"""
Programme qui permet de résumer les resultats de precision et rappel 
pour les Noms et les Verbes générés par les différents modèles.
"""

def get_plot(fic_v0_i, fic_v1_i, fic_v2_i, fic_v3_i, fic_v4_i, fic_v5_i, fic_vm_i,
             fic_v0_g, fic_v1_g, fic_v2_g, fic_v3_g, fic_v4_g, fic_v5_g, fic_vm_g,
             fic_v0_d, fic_v1_d, fic_v2_d, fic_v3_d, fic_v4_d, fic_v5_d, fic_vm_d,
             fic_v0_b, fic_v1_b, fic_v2_b, fic_v3_b, fic_v4_b, fic_v5_b, fic_vm_b):
    
    v0_i = pd.DataFrame.from_csv(fic_v0_i, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v1_i = pd.DataFrame.from_csv(fic_v1_i, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v2_i = pd.DataFrame.from_csv(fic_v2_i, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v3_i = pd.DataFrame.from_csv(fic_v3_i, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v4_i = pd.DataFrame.from_csv(fic_v4_i, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v5_i = pd.DataFrame.from_csv(fic_v5_i, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    vm_i = pd.DataFrame.from_csv(fic_vm_i, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    
    """
    chargement fichiers modèle gauche
    """

    
    v0_g = pd.DataFrame.from_csv(fic_v0_g, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v1_g = pd.DataFrame.from_csv(fic_v1_g, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v2_g = pd.DataFrame.from_csv(fic_v2_g, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v3_g = pd.DataFrame.from_csv(fic_v3_g, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v4_g = pd.DataFrame.from_csv(fic_v4_g, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v5_g = pd.DataFrame.from_csv(fic_v5_g, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    vm_g = pd.DataFrame.from_csv(fic_vm_g, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    
    """
    chargement fichiers modèle droit
    """
    
    v0_d = pd.DataFrame.from_csv(fic_v0_d, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v1_d = pd.DataFrame.from_csv(fic_v1_d, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v2_d = pd.DataFrame.from_csv(fic_v2_d, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v3_d = pd.DataFrame.from_csv(fic_v3_d, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v4_d = pd.DataFrame.from_csv(fic_v4_d, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v5_d = pd.DataFrame.from_csv(fic_v5_d, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    vm_d = pd.DataFrame.from_csv(fic_vm_d, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    
    """
    chargement fichiers modèle base-line
    """
    
    v0_b = pd.DataFrame.from_csv(fic_v0_b, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v1_b = pd.DataFrame.from_csv(fic_v1_b, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v2_b = pd.DataFrame.from_csv(fic_v2_b, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v3_b = pd.DataFrame.from_csv(fic_v3_b, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v4_b = pd.DataFrame.from_csv(fic_v4_b, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    v5_b = pd.DataFrame.from_csv(fic_v5_b, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    vm_b = pd.DataFrame.from_csv(fic_vm_b, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
    
    
    """
    calculer la moyenne des plis de la validation croisée du modèle imbriqué
    """
    
    mean_v0_i = v0_i.mean(0)
    mean_v1_i = v1_i.mean(0)
    mean_v2_i = v2_i.mean(0)
    mean_v3_i = v3_i.mean(0)
    mean_v4_i = v4_i.mean(0)
    mean_v5_i = v5_i.mean(0)
    mean_vm_i = vm_i.mean(0)
    
    """
    calculer la moyenne des plis de la validation croisée du modèle gauche
    """
    
    mean_v0_g = v0_g.mean(0)
    mean_v1_g = v1_g.mean(0)
    mean_v2_g = v2_g.mean(0)
    mean_v3_g = v3_g.mean(0)
    mean_v4_g = v4_g.mean(0)
    mean_v5_g = v5_g.mean(0)
    mean_vm_g = vm_g.mean(0)
    
    """
    calculer la moyenne des plis de la validation croisée du modèle droit
    """
    
    mean_v0_d = v0_d.mean(0)
    mean_v1_d = v1_d.mean(0)
    mean_v2_d = v2_d.mean(0)
    mean_v3_d = v3_d.mean(0)
    mean_v4_d = v4_d.mean(0)
    mean_v5_d = v5_d.mean(0)
    mean_vm_d = vm_d.mean(0)
    
    """
    calculer la moyenne des plis de la validation croisée du modèle base-line
    """
    
    mean_v0_b = v0_b.mean(0)
    mean_v1_b = v1_b.mean(0)
    mean_v2_b = v2_b.mean(0)
    mean_v3_b = v3_b.mean(0)
    mean_v4_b = v4_b.mean(0)
    mean_v5_b = v5_b.mean(0)
    mean_vm_b = vm_b.mean(0)
    
    """
    calculer l'erreur standard des plis de la validation croisée du modèle imbriqué
    """
    
    sem_v0_i = v0_i.sem(0)
    sem_v1_i = v1_i.sem(0)
    sem_v2_i = v2_i.sem(0)
    sem_v3_i = v3_i.sem(0)
    sem_v4_i = v4_i.sem(0)
    sem_v5_i = v5_i.sem(0)
    sem_vm_i = vm_i.sem(0)

    """
    calculer l'erreur standard des plis de la validation croisée du modèle gauche
    """
   
    sem_v0_g = v0_g.sem(0)
    sem_v1_g = v1_g.sem(0)
    sem_v2_g = v2_g.sem(0)
    sem_v3_g = v3_g.sem(0)
    sem_v4_g = v4_g.sem(0)
    sem_v5_g = v5_g.sem(0)
    sem_vm_g = vm_g.sem(0)

    """
    calculer l'erreur standard des plis de la validation croisée du modèle droit
    """
  
    sem_v0_d = v0_d.sem(0)
    sem_v1_d = v1_d.sem(0)
    sem_v2_d = v2_d.sem(0)
    sem_v3_d = v3_d.sem(0)
    sem_v4_d = v4_d.sem(0)
    sem_v5_d = v5_d.sem(0)
    sem_vm_d = vm_d.sem(0)
    
    
    """
    calculer l'erreur standard des plis de la validation croisée du modèle base-line
    """
  
    sem_v0_b = v0_b.sem(0)
    sem_v1_b = v1_b.sem(0)
    sem_v2_b = v2_b.sem(0)
    sem_v3_b = v3_b.sem(0)
    sem_v4_b = v4_b.sem(0)
    sem_v5_b = v5_b.sem(0)
    sem_vm_b = vm_b.sem(0)

    """
    Calculer la précision pour les Noms pour le modèle imbriqué
    """
    means_pre_n_i = {}
    means_pre_n_i['v0']=mean_v0_i[['precision_n']]
    means_pre_n_i['v1']=mean_v1_i[['precision_n']]
    means_pre_n_i['v2']=mean_v2_i[['precision_n']]
    means_pre_n_i['v3']=mean_v3_i[['precision_n']]
    means_pre_n_i['v4']=mean_v4_i[['precision_n']]
    means_pre_n_i['v5']=mean_v5_i[['precision_n']]
    means_pre_n_i['vm']=mean_vm_i[['precision_n']]   
    means_pre_n_i = pd.DataFrame(means_pre_n_i)
    
    
    """
    Calculer la précision pour les Noms du modèle gauche
    """
    means_pre_n_g = {}
    means_pre_n_g['v0']=mean_v0_g[['precision_n']]
    means_pre_n_g['v1']=mean_v1_g[['precision_n']]
    means_pre_n_g['v2']=mean_v2_g[['precision_n']]
    means_pre_n_g['v3']=mean_v3_g[['precision_n']]
    means_pre_n_g['v4']=mean_v4_g[['precision_n']]
    means_pre_n_g['v5']=mean_v5_g[['precision_n']]
    means_pre_n_g['vm']=mean_vm_g[['precision_n']]   
    means_pre_n_g = pd.DataFrame(means_pre_n_g)

    """
    Calculer la précision pour les Noms du modèle droit
    """
    means_pre_n_d = {}
    means_pre_n_d['v0']=mean_v0_d[['precision_n']]
    means_pre_n_d['v1']=mean_v1_d[['precision_n']]
    means_pre_n_d['v2']=mean_v2_d[['precision_n']]
    means_pre_n_d['v3']=mean_v3_d[['precision_n']]
    means_pre_n_d['v4']=mean_v4_d[['precision_n']]
    means_pre_n_d['v5']=mean_v5_d[['precision_n']]
    means_pre_n_d['vm']=mean_vm_d[['precision_n']]   
    means_pre_n_d = pd.DataFrame(means_pre_n_d)
    

    """
    Calculer la précision pour les Noms du modèle base-line
    """
    means_pre_n_b = {}
    means_pre_n_b['v0']=mean_v0_b[['precision_n']]
    means_pre_n_b['v1']=mean_v1_b[['precision_n']]
    means_pre_n_b['v2']=mean_v2_b[['precision_n']]
    means_pre_n_b['v3']=mean_v3_b[['precision_n']]
    means_pre_n_b['v4']=mean_v4_b[['precision_n']]
    means_pre_n_b['v5']=mean_v5_b[['precision_n']]
    means_pre_n_b['vm']=mean_vm_b[['precision_n']]   
    means_pre_n_b = pd.DataFrame(means_pre_n_b)
    
    
    """
    calculer l'erreur standard pour la précision des Noms du modèle imbriqué
    """
    semevs_pre_n_i = pd.DataFrame()
    semevs_pre_n_i['v0']=sem_v0_i[['precision_n']]
    semevs_pre_n_i['v1']=sem_v1_i[['precision_n']]
    semevs_pre_n_i['v2']=sem_v2_i[['precision_n']]
    semevs_pre_n_i['v3']=sem_v3_i[['precision_n']]
    semevs_pre_n_i['v4']=sem_v4_i[['precision_n']]
    semevs_pre_n_i['v5']=sem_v5_i[['precision_n']]
    semevs_pre_n_i['vm']=sem_vm_i[['precision_n']]
    
    
    """
    calculer l'erreur standard type pour la précision des Noms du modèle gauche
    """
    semevs_pre_n_g = pd.DataFrame()
    semevs_pre_n_g['v0']=sem_v0_g[['precision_n']]
    semevs_pre_n_g['v1']=sem_v1_g[['precision_n']]
    semevs_pre_n_g['v2']=sem_v2_g[['precision_n']]
    semevs_pre_n_g['v3']=sem_v3_g[['precision_n']]
    semevs_pre_n_g['v4']=sem_v4_g[['precision_n']]
    semevs_pre_n_g['v5']=sem_v5_g[['precision_n']]
    semevs_pre_n_g['vm']=sem_vm_g[['precision_n']]
    
    """
    calculer l'erreur standard pour la précision des Noms du modèle droit
    """
    semevs_pre_n_d = pd.DataFrame()
    semevs_pre_n_d['v0']=sem_v0_d[['precision_n']]
    semevs_pre_n_d['v1']=sem_v1_d[['precision_n']]
    semevs_pre_n_d['v2']=sem_v2_d[['precision_n']]
    semevs_pre_n_d['v3']=sem_v3_d[['precision_n']]
    semevs_pre_n_d['v4']=sem_v4_d[['precision_n']]
    semevs_pre_n_d['v5']=sem_v5_d[['precision_n']]
    semevs_pre_n_d['vm']=sem_vm_d[['precision_n']]
    
    
    """
    calculer l'erreur standard pour la précision des Noms du modèle base-line
    """
    semevs_pre_n_b = pd.DataFrame()
    semevs_pre_n_b['v0']=sem_v0_b[['precision_n']]
    semevs_pre_n_b['v1']=sem_v1_b[['precision_n']]
    semevs_pre_n_b['v2']=sem_v2_b[['precision_n']]
    semevs_pre_n_b['v3']=sem_v3_b[['precision_n']]
    semevs_pre_n_b['v4']=sem_v4_b[['precision_n']]
    semevs_pre_n_b['v5']=sem_v5_b[['precision_n']]
    semevs_pre_n_b['vm']=sem_vm_b[['precision_n']]
    
    """
    Calculer la précision pour les Verbes pour le modèle imbriqué
    """
    means_pre_v_i = {}
    means_pre_v_i['v0']=mean_v0_i[['precision_v']]
    means_pre_v_i['v1']=mean_v1_i[['precision_v']]
    means_pre_v_i['v2']=mean_v2_i[['precision_v']]
    means_pre_v_i['v3']=mean_v3_i[['precision_v']]
    means_pre_v_i['v4']=mean_v4_i[['precision_v']]
    means_pre_v_i['v5']=mean_v5_i[['precision_v']]
    means_pre_v_i['vm']=mean_vm_i[['precision_v']]   
    means_pre_v_i = pd.DataFrame(means_pre_v_i)

    """
    Calculer la précision pour les Verbes pour le modèle gauche
    """
    means_pre_v_g = {}
    means_pre_v_g['v0']=mean_v0_g[['precision_v']]
    means_pre_v_g['v1']=mean_v1_g[['precision_v']]
    means_pre_v_g['v2']=mean_v2_g[['precision_v']]
    means_pre_v_g['v3']=mean_v3_g[['precision_v']]
    means_pre_v_g['v4']=mean_v4_g[['precision_v']]
    means_pre_v_g['v5']=mean_v5_g[['precision_v']]
    means_pre_v_g['vm']=mean_vm_g[['precision_v']]   
    means_pre_v_g = pd.DataFrame(means_pre_v_g)
    
    """
    Calculer la précision pour les Verbes pour le modèle droit
    """
    means_pre_v_d = {}
    means_pre_v_d['v0']=mean_v0_d[['precision_v']]
    means_pre_v_d['v1']=mean_v1_d[['precision_v']]
    means_pre_v_d['v2']=mean_v2_d[['precision_v']]
    means_pre_v_d['v3']=mean_v3_d[['precision_v']]
    means_pre_v_d['v4']=mean_v4_d[['precision_v']]
    means_pre_v_d['v5']=mean_v5_d[['precision_v']]
    means_pre_v_d['vm']=mean_vm_d[['precision_v']]   
    means_pre_v_d = pd.DataFrame(means_pre_v_d)
    
    
    """
    Calculer la précision pour les Verbes pour le modèle base-line
    """
    means_pre_v_b = {}
    means_pre_v_b['v0']=mean_v0_b[['precision_v']]
    means_pre_v_b['v1']=mean_v1_b[['precision_v']]
    means_pre_v_b['v2']=mean_v2_b[['precision_v']]
    means_pre_v_b['v3']=mean_v3_b[['precision_v']]
    means_pre_v_b['v4']=mean_v4_b[['precision_v']]
    means_pre_v_b['v5']=mean_v5_b[['precision_v']]
    means_pre_v_b['vm']=mean_vm_b[['precision_v']]   
    means_pre_v_b = pd.DataFrame(means_pre_v_b)

    """
    Calculer l'erreur standard pour les Verbes pour le modèle imbriqué
    """
    semevs_pre_v_i = pd.DataFrame()
    semevs_pre_v_i['v0']=sem_v0_i[['precision_v']]
    semevs_pre_v_i['v1']=sem_v1_i[['precision_v']]
    semevs_pre_v_i['v2']=sem_v2_i[['precision_v']]
    semevs_pre_v_i['v3']=sem_v3_i[['precision_v']] 
    semevs_pre_v_i['v4']=sem_v4_i[['precision_v']]
    semevs_pre_v_i['v5']=sem_v5_i[['precision_v']]   
    semevs_pre_v_i['vm']=sem_vm_i[['precision_v']]

    """
    Calculer l'erreur standard pour les Verbes pour le modèle gauche
    """    
    semevs_pre_v_g = pd.DataFrame()
    semevs_pre_v_g['v0']=sem_v0_g[['precision_v']]
    semevs_pre_v_g['v1']=sem_v1_g[['precision_v']]
    semevs_pre_v_g['v2']=sem_v2_g[['precision_v']]
    semevs_pre_v_g['v3']=sem_v3_g[['precision_v']] 
    semevs_pre_v_g['v4']=sem_v4_g[['precision_v']]
    semevs_pre_v_g['v5']=sem_v5_g[['precision_v']] 
    semevs_pre_v_g['vm']=sem_vm_g[['precision_v']]
    
    """
    Calculer l'erreur standard pour les Verbes pour le modèle droit
    """
    semevs_pre_v_d = pd.DataFrame()
    semevs_pre_v_d['v0']=sem_v0_d[['precision_v']]
    semevs_pre_v_d['v1']=sem_v1_d[['precision_v']]
    semevs_pre_v_d['v2']=sem_v2_d[['precision_v']]
    semevs_pre_v_d['v3']=sem_v3_d[['precision_v']] 
    semevs_pre_v_d['v4']=sem_v4_d[['precision_v']]
    semevs_pre_v_d['v5']=sem_v5_d[['precision_v']] 
    semevs_pre_v_d['vm']=sem_vm_d[['precision_v']]
    
    """
    Calculer l'erreur standard pour les Verbes pour le modèle base-line
    """
    semevs_pre_v_b = pd.DataFrame()
    semevs_pre_v_b['v0']=sem_v0_b[['precision_v']]
    semevs_pre_v_b['v1']=sem_v1_b[['precision_v']]
    semevs_pre_v_b['v2']=sem_v2_b[['precision_v']]
    semevs_pre_v_b['v3']=sem_v3_b[['precision_v']] 
    semevs_pre_v_b['v4']=sem_v4_b[['precision_v']]
    semevs_pre_v_b['v5']=sem_v5_b[['precision_v']] 
    semevs_pre_v_b['vm']=sem_vm_b[['precision_v']]
    
    """
    Calculer le rappel pour les Noms du modèle imbriqué
    """
    means_rap_n_i = {}
    means_rap_n_i['v0']=mean_v0_i[['rappel_n']]
    means_rap_n_i['v1']=mean_v1_i[['rappel_n']]
    means_rap_n_i['v2']=mean_v2_i[['rappel_n']]
    means_rap_n_i['v3']=mean_v3_i[['rappel_n']]
    means_rap_n_i['v4']=mean_v4_i[['rappel_n']]
    means_rap_n_i['v5']=mean_v5_i[['rappel_n']]
    means_rap_n_i['vm']=mean_vm_i[['rappel_n']]   
    means_rap_n_i = pd.DataFrame(means_rap_n_i)
 
    """
    Calculer le rappel pour les Noms du modèle gauche
    """   
    means_rap_n_g = {}
    means_rap_n_g['v0']=mean_v0_g[['rappel_n']]
    means_rap_n_g['v1']=mean_v1_g[['rappel_n']]
    means_rap_n_g['v2']=mean_v2_g[['rappel_n']]
    means_rap_n_g['v3']=mean_v3_g[['rappel_n']]
    means_rap_n_g['v4']=mean_v4_g[['rappel_n']]
    means_rap_n_g['v5']=mean_v5_g[['rappel_n']]    
    means_rap_n_g['vm']=mean_vm_g[['rappel_n']]   
    means_rap_n_g = pd.DataFrame(means_rap_n_g)
    
    """
    Calculer le rappel pour les Noms du modèle droit
    """
    means_rap_n_d = {}
    means_rap_n_d['v0']=mean_v0_d[['rappel_n']]
    means_rap_n_d['v1']=mean_v1_d[['rappel_n']]
    means_rap_n_d['v2']=mean_v2_d[['rappel_n']]
    means_rap_n_d['v3']=mean_v3_d[['rappel_n']]
    means_rap_n_d['v4']=mean_v4_d[['rappel_n']]
    means_rap_n_d['v5']=mean_v5_d[['rappel_n']]
    means_rap_n_d['vm']=mean_vm_d[['rappel_n']]   
    means_rap_n_d = pd.DataFrame(means_rap_n_d)
    
    """
    Calculer le rappel pour les Noms du modèle base-line
    """
    means_rap_n_b = {}
    means_rap_n_b['v0']=mean_v0_b[['rappel_n']]
    means_rap_n_b['v1']=mean_v1_b[['rappel_n']]
    means_rap_n_b['v2']=mean_v2_b[['rappel_n']]
    means_rap_n_b['v3']=mean_v3_b[['rappel_n']]
    means_rap_n_b['v4']=mean_v4_b[['rappel_n']]
    means_rap_n_b['v5']=mean_v5_b[['rappel_n']]
    means_rap_n_b['vm']=mean_vm_b[['rappel_n']]   
    means_rap_n_b = pd.DataFrame(means_rap_n_b)
    
    """
    Calculer l'erreur standard du rapel pour les Noms du modèle imbriqué
    """
    semevs_rap_n_i = pd.DataFrame()
    semevs_rap_n_i['v0']=sem_v0_i[['rappel_n']]
    semevs_rap_n_i['v1']=sem_v1_i[['rappel_n']]
    semevs_rap_n_i['v2']=sem_v2_i[['rappel_n']]
    semevs_rap_n_i['v3']=sem_v3_i[['rappel_n']]
    semevs_rap_n_i['v4']=sem_v4_i[['rappel_n']]
    semevs_rap_n_i['v5']=sem_v5_i[['rappel_n']]
    semevs_rap_n_i['vm']=sem_vm_i[['rappel_n']]

    """
    Calculer l'erreur standard du rapel pour les Noms du modèle gauche
    """
    semevs_rap_n_g = pd.DataFrame()
    semevs_rap_n_g['v0']=sem_v0_g[['rappel_n']]
    semevs_rap_n_g['v1']=sem_v1_g[['rappel_n']]
    semevs_rap_n_g['v2']=sem_v2_g[['rappel_n']]
    semevs_rap_n_g['v3']=sem_v3_i[['rappel_n']]
    semevs_rap_n_g['v4']=sem_v4_i[['rappel_n']]
    semevs_rap_n_g['v5']=sem_v5_i[['rappel_n']]
    semevs_rap_n_g['vm']=sem_vm_g[['rappel_n']]

    """
    Calculer l'erreur standard type du rapel pour les Noms du modèle droit
    """
    semevs_rap_n_d = pd.DataFrame()
    semevs_rap_n_d['v0']=sem_v0_d[['rappel_n']]
    semevs_rap_n_d['v1']=sem_v1_d[['rappel_n']]
    semevs_rap_n_d['v2']=sem_v2_d[['rappel_n']]
    semevs_rap_n_d['v3']=sem_v3_d[['rappel_n']]
    semevs_rap_n_d['v4']=sem_v4_d[['rappel_n']]
    semevs_rap_n_d['v5']=sem_v5_d[['rappel_n']]
    semevs_rap_n_d['vm']=sem_vm_d[['rappel_n']]
    
    """
    Calculer l'erreur standard type du rapel pour les Noms du modèle base-line
    """
    semevs_rap_n_b = pd.DataFrame()
    semevs_rap_n_b['v0']=sem_v0_b[['rappel_n']]
    semevs_rap_n_b['v1']=sem_v1_b[['rappel_n']]
    semevs_rap_n_b['v2']=sem_v2_b[['rappel_n']]
    semevs_rap_n_b['v3']=sem_v3_b[['rappel_n']]
    semevs_rap_n_b['v4']=sem_v4_b[['rappel_n']]
    semevs_rap_n_b['v5']=sem_v5_b[['rappel_n']]
    semevs_rap_n_b['vm']=sem_vm_b[['rappel_n']]

    """
    Calculer le rappel pour les Verbes du modèle imbriqué
    """
    means_rap_v_i = {}
    means_rap_v_i['v0']=mean_v0_i[['rappel_v']]
    means_rap_v_i['v1']=mean_v1_i[['rappel_v']]
    means_rap_v_i['v2']=mean_v2_i[['rappel_v']]
    means_rap_v_i['v3']=mean_v3_i[['rappel_v']]
    means_rap_v_i['v4']=mean_v4_i[['rappel_v']]
    means_rap_v_i['v5']=mean_v5_i[['rappel_v']]
    means_rap_v_i['vm']=mean_vm_i[['rappel_v']]   
    means_rap_v_i = pd.DataFrame(means_rap_v_i)
    
    """
    Calculer le rappel pour les Verbes du modèle gauche
    """    
    means_rap_v_g = {}
    means_rap_v_g['v0']=mean_v0_g[['rappel_v']]
    means_rap_v_g['v1']=mean_v1_g[['rappel_v']]
    means_rap_v_g['v2']=mean_v2_g[['rappel_v']]
    means_rap_v_g['v3']=mean_v3_g[['rappel_v']]
    means_rap_v_g['v4']=mean_v4_g[['rappel_v']]
    means_rap_v_g['v5']=mean_v5_g[['rappel_v']]
    means_rap_v_g['vm']=mean_vm_g[['rappel_v']]   
    means_rap_v_g = pd.DataFrame(means_rap_v_g)
    
    """
    Calculer le rappel pour les Verbes du modèle droit
    """
    means_rap_v_d = {}
    means_rap_v_d['v0']=mean_v0_d[['rappel_v']]
    means_rap_v_d['v1']=mean_v1_d[['rappel_v']]
    means_rap_v_d['v2']=mean_v2_d[['rappel_v']]
    means_rap_v_d['v3']=mean_v3_d[['rappel_v']]
    means_rap_v_d['v4']=mean_v4_d[['rappel_v']]
    means_rap_v_d['v5']=mean_v5_d[['rappel_v']]
    means_rap_v_d['vm']=mean_vm_d[['rappel_v']]   
    means_rap_v_d = pd.DataFrame(means_rap_v_d)
    
    """
    Calculer le rappel pour les Verbes du modèle base-line
    """
    means_rap_v_b = {}
    means_rap_v_b['v0']=mean_v0_b[['rappel_v']]
    means_rap_v_b['v1']=mean_v1_b[['rappel_v']]
    means_rap_v_b['v2']=mean_v2_b[['rappel_v']]
    means_rap_v_b['v3']=mean_v3_b[['rappel_v']]
    means_rap_v_b['v4']=mean_v4_b[['rappel_v']]
    means_rap_v_b['v5']=mean_v5_b[['rappel_v']]
    means_rap_v_b['vm']=mean_vm_b[['rappel_v']]   
    means_rap_v_b = pd.DataFrame(means_rap_v_b)
    
    """
    Calculer l'écart type du rappel pour les Verbes du modèle imbriqué
    """
    semevs_rap_v_i = pd.DataFrame()
    semevs_rap_v_i['v0']=sem_v0_i[['rappel_v']]
    semevs_rap_v_i['v1']=sem_v1_i[['rappel_v']]
    semevs_rap_v_i['v2']=sem_v2_i[['rappel_v']]
    semevs_rap_v_i['v3']=sem_v3_i[['rappel_v']]
    semevs_rap_v_i['v4']=sem_v4_i[['rappel_v']]
    semevs_rap_v_i['v5']=sem_v5_i[['rappel_v']]
    semevs_rap_v_i['vm']=sem_vm_i[['rappel_v']]
    
    """
    Calculer l'erreur standard du rappel pour les Verbes du modèle gauche
    """
    semevs_rap_v_g = pd.DataFrame()
    semevs_rap_v_g['v0']=sem_v0_g[['rappel_v']]
    semevs_rap_v_g['v1']=sem_v1_g[['rappel_v']]
    semevs_rap_v_g['v3']=sem_v3_g[['rappel_v']]
    semevs_rap_v_g['v4']=sem_v4_g[['rappel_v']]
    semevs_rap_v_g['v5']=sem_v5_g[['rappel_v']]
    semevs_rap_v_g['v2']=sem_v2_g[['rappel_v']]
    semevs_rap_v_g['vm']=sem_vm_g[['rappel_v']]

    """
    Calculer l'erreur standard du rappel pour les Verbes du modèle droit
    """
    semevs_rap_v_d = pd.DataFrame()
    semevs_rap_v_d['v0']=sem_v0_d[['rappel_v']]
    semevs_rap_v_d['v1']=sem_v1_d[['rappel_v']]
    semevs_rap_v_d['v2']=sem_v2_d[['rappel_v']]
    semevs_rap_v_d['v3']=sem_v3_d[['rappel_v']]
    semevs_rap_v_d['v4']=sem_v4_d[['rappel_v']]
    semevs_rap_v_d['v5']=sem_v5_d[['rappel_v']]
    semevs_rap_v_d['vm']=sem_vm_d[['rappel_v']]
    
    """
    Calculer l'erreur standard du rappel pour les Verbes du modèle base-line
    """
    semevs_rap_v_b = pd.DataFrame()
    semevs_rap_v_b['v0']=sem_v0_b[['rappel_v']]
    semevs_rap_v_b['v1']=sem_v1_b[['rappel_v']]
    semevs_rap_v_b['v2']=sem_v2_b[['rappel_v']]
    semevs_rap_v_b['v3']=sem_v3_b[['rappel_v']]
    semevs_rap_v_b['v4']=sem_v4_b[['rappel_v']]
    semevs_rap_v_b['v5']=sem_v5_b[['rappel_v']]
    semevs_rap_v_b['vm']=sem_vm_b[['rappel_v']]
    
    """
    Calculer le nombre de prédictions pour les trigrammes du modèle imbriqué
    """
    means_tri_i = {}
    means_tri_i['v0']=mean_v0_i[['nb_tri']]
    means_tri_i['v1']=mean_v1_i[['nb_tri']]
    means_tri_i['v2']=mean_v2_i[['nb_tri']]
    means_tri_i['v3']=mean_v3_i[['nb_tri']]
    means_tri_i['v4']=mean_v4_i[['nb_tri']]
    means_tri_i['v5']=mean_v5_i[['nb_tri']]
    means_tri_i['vm']=mean_vm_i[['nb_tri']]   
    means_tri_i = pd.DataFrame(means_tri_i)
    
    """
    Calculer le nombre de prédictions pour les bigrammes du modèle imbriqué
    """
    means_bi_i = {}
    means_bi_i['v0']=mean_v0_i[['nb_bi']]
    means_bi_i['v1']=mean_v1_i[['nb_bi']]
    means_bi_i['v2']=mean_v2_i[['nb_bi']]
    means_bi_i['v3']=mean_v3_i[['nb_bi']]
    means_bi_i['v4']=mean_v4_i[['nb_bi']]
    means_bi_i['v5']=mean_v5_i[['nb_bi']]
    means_bi_i['vm']=mean_vm_i[['nb_bi']]   
    means_bi_i = pd.DataFrame(means_bi_i)
    
    """
    Calculer le nombre de fois que le modèle imbriqué n'a rien prédit
    """
    means_none_i = {}
    means_none_i['v0']=mean_v0_i[['nb_none']]
    means_none_i['v1']=mean_v1_i[['nb_none']]
    means_none_i['v2']=mean_v2_i[['nb_none']]
    means_none_i['v3']=mean_v3_i[['nb_none']]
    means_none_i['v4']=mean_v4_i[['nb_none']]
    means_none_i['v5']=mean_v5_i[['nb_none']]
    means_none_i['vm']=mean_vm_i[['nb_none']]   
    means_none_i = pd.DataFrame(means_none_i)
    
    """
    nombre de prédictions modèle gauche
    """
    
    means_tri_g = {}
    means_tri_g['v0']=mean_v0_g[['nb_tri']]
    means_tri_g['v1']=mean_v1_g[['nb_tri']]
    means_tri_g['v2']=mean_v2_g[['nb_tri']]
    means_tri_g['v3']=mean_v3_g[['nb_tri']]
    means_tri_g['v4']=mean_v4_g[['nb_tri']]
    means_tri_g['v5']=mean_v5_g[['nb_tri']]
    means_tri_g['vm']=mean_vm_g[['nb_tri']]   
    means_tri_g = pd.DataFrame(means_tri_g)
    
    means_bi_g = {}
    means_bi_g['v0']=mean_v0_g[['nb_bi']]
    means_bi_g['v1']=mean_v1_g[['nb_bi']]
    means_bi_g['v2']=mean_v2_g[['nb_bi']]
    means_bi_g['v3']=mean_v3_g[['nb_bi']]
    means_bi_g['v4']=mean_v4_g[['nb_bi']]
    means_bi_g['v5']=mean_v5_g[['nb_bi']]
    means_bi_g['vm']=mean_vm_g[['nb_bi']]   
    means_bi_g = pd.DataFrame(means_bi_g)
    
    means_none_g = {}
    means_none_g['v0']=mean_v0_g[['nb_none']]
    means_none_g['v1']=mean_v1_g[['nb_none']]
    means_none_g['v2']=mean_v2_g[['nb_none']]
    means_none_g['v3']=mean_v3_g[['nb_none']]
    means_none_g['v4']=mean_v4_g[['nb_none']]
    means_none_g['v5']=mean_v5_g[['nb_none']]
    means_none_g['vm']=mean_vm_g[['nb_none']]   
    means_none_g = pd.DataFrame(means_none_g)

    """
    nombre de prédictions pour le modèle droit
    """
    
    means_tri_d = {}
    means_tri_d['v0']=mean_v0_d[['nb_tri']]
    means_tri_d['v1']=mean_v1_d[['nb_tri']]
    means_tri_d['v2']=mean_v2_d[['nb_tri']]
    means_tri_d['v3']=mean_v3_d[['nb_tri']]
    means_tri_d['v4']=mean_v4_d[['nb_tri']]
    means_tri_d['v5']=mean_v5_d[['nb_tri']]
    means_tri_d['vm']=mean_vm_d[['nb_tri']]   
    means_tri_d = pd.DataFrame(means_tri_d)
    
    means_bi_d = {}
    means_bi_d['v0']=mean_v0_d[['nb_bi']]
    means_bi_d['v1']=mean_v1_d[['nb_bi']]
    means_bi_d['v2']=mean_v2_d[['nb_bi']]
    means_bi_d['v3']=mean_v3_d[['nb_bi']]
    means_bi_d['v4']=mean_v4_d[['nb_bi']]
    means_bi_d['v5']=mean_v5_d[['nb_bi']]
    means_bi_d['vm']=mean_vm_d[['nb_bi']]   
    means_bi_d = pd.DataFrame(means_bi_d)
    
    means_none_d = {}
    means_none_d['v0']=mean_v0_d[['nb_none']]
    means_none_d['v1']=mean_v1_d[['nb_none']]
    means_none_d['v2']=mean_v2_d[['nb_none']]
    means_none_d['v3']=mean_v3_d[['nb_none']]
    means_none_d['v4']=mean_v4_d[['nb_none']]
    means_none_d['v5']=mean_v5_d[['nb_none']]
    means_none_d['vm']=mean_vm_d[['nb_none']]   
    means_none_d = pd.DataFrame(means_none_d)
    
    
#     """
#     nombre de prédictions pour le modèle base-line
#     """
#     
#     means_tri_b = {}
#     means_tri_b['v0']=mean_v0_b[['nb_tri']]
#     means_tri_b['v1']=mean_v1_b[['nb_tri']]
#     means_tri_b['v2']=mean_v2_b[['nb_tri']]
#     means_tri_b['v3']=mean_v3_b[['nb_tri']]
#     means_tri_b['v4']=mean_v4_b[['nb_tri']]
#     means_tri_b['v5']=mean_v5_b[['nb_tri']]
#     means_tri_b['vm']=mean_vm_b[['nb_tri']]   
#     means_tri_b = pd.DataFrame(means_tri_b)
#     
#     means_bi_b = {}
#     means_bi_b['v0']=mean_v0_b[['nb_bi']]
#     means_bi_b['v1']=mean_v1_b[['nb_bi']]
#     means_bi_b['v2']=mean_v2_b[['nb_bi']]
#     means_bi_b['v3']=mean_v3_b[['nb_bi']]
#     means_bi_b['v4']=mean_v4_b[['nb_bi']]
#     means_bi_b['v5']=mean_v5_b[['nb_bi']]
#     means_bi_b['vm']=mean_vm_b[['nb_bi']]   
#     means_bi_b = pd.DataFrame(means_bi_b)
#     
#     means_none_b = {}
#     means_none_b['v0']=mean_v0_b[['nb_none']]
#     means_none_b['v1']=mean_v1_b[['nb_none']]
#     means_none_b['v2']=mean_v2_b[['nb_none']]
#     means_none_b['v3']=mean_v3_b[['nb_none']]
#     means_none_b['v4']=mean_v4_b[['nb_none']]
#     means_none_b['v5']=mean_v5_b[['nb_none']]
#     means_none_b['vm']=mean_vm_b[['nb_none']]   
#     means_none_b = pd.DataFrame(means_none_b)
    
    """
    erreur standard trigrammes
    """

    semevs_tri_i = {}
    semevs_tri_i['v0']=sem_v0_i[['nb_tri']]
    semevs_tri_i['v1']=sem_v1_i[['nb_tri']]
    semevs_tri_i['v2']=sem_v2_i[['nb_tri']]
    semevs_tri_i['v3']=sem_v3_i[['nb_tri']]
    semevs_tri_i['v4']=sem_v4_i[['nb_tri']]
    semevs_tri_i['v5']=sem_v5_i[['nb_tri']]
    semevs_tri_i['vm']=sem_vm_i[['nb_tri']]
    semevs_tri_i = pd.DataFrame(semevs_tri_i)
    
    semevs_tri_g = {}
    semevs_tri_g['v0']=sem_v0_g[['nb_tri']]
    semevs_tri_g['v1']=sem_v1_g[['nb_tri']]
    semevs_tri_g['v2']=sem_v2_g[['nb_tri']]
    semevs_tri_g['v3']=sem_v3_g[['nb_tri']]
    semevs_tri_g['v4']=sem_v4_g[['nb_tri']]
    semevs_tri_g['v5']=sem_v5_g[['nb_tri']]
    semevs_tri_g['vm']=sem_vm_g[['nb_tri']]
    semevs_tri_g = pd.DataFrame(semevs_tri_g)
    
    semevs_tri_d = {}
    semevs_tri_d['v0']=sem_v0_d[['nb_tri']]
    semevs_tri_d['v1']=sem_v1_d[['nb_tri']]
    semevs_tri_d['v2']=sem_v2_d[['nb_tri']]
    semevs_tri_d['v3']=sem_v3_d[['nb_tri']]
    semevs_tri_d['v4']=sem_v4_d[['nb_tri']]
    semevs_tri_d['v5']=sem_v5_d[['nb_tri']]
    semevs_tri_d['vm']=sem_vm_d[['nb_tri']]
    semevs_tri_d = pd.DataFrame(semevs_tri_d)
    
    """
    calculer erreur standard bigrammes
    """
    
    semevs_bi_i = {}
    semevs_bi_i['v0']=sem_v0_i[['nb_bi']]
    semevs_bi_i['v1']=sem_v1_i[['nb_bi']]
    semevs_bi_i['v2']=sem_v2_i[['nb_bi']]
    semevs_bi_i['v3']=sem_v3_i[['nb_bi']]
    semevs_bi_i['v4']=sem_v4_i[['nb_bi']]
    semevs_bi_i['v5']=sem_v5_i[['nb_bi']]
    semevs_bi_i['vm']=sem_vm_i[['nb_bi']]
    semevs_bi_i = pd.DataFrame(semevs_bi_i)
    
    semevs_bi_g ={}
    semevs_bi_g['v0']=sem_v0_g[['nb_bi']]
    semevs_bi_g['v1']=sem_v1_g[['nb_bi']]
    semevs_bi_g['v2']=sem_v2_g[['nb_bi']]
    semevs_bi_g['v3']=sem_v3_g[['nb_bi']]
    semevs_bi_g['v4']=sem_v4_g[['nb_bi']]
    semevs_bi_g['v5']=sem_v5_g[['nb_bi']]
    semevs_bi_g['vm']=sem_vm_g[['nb_bi']]
    semevs_bi_g = pd.DataFrame(semevs_bi_g)
    
    semevs_bi_d = {}
    semevs_bi_d['v0']=sem_v0_d[['nb_bi']]
    semevs_bi_d['v1']=sem_v1_d[['nb_bi']]
    semevs_bi_d['v2']=sem_v2_d[['nb_bi']]
    semevs_bi_d['v3']=sem_v3_d[['nb_bi']]
    semevs_bi_d['v4']=sem_v4_d[['nb_bi']]
    semevs_bi_d['v5']=sem_v5_d[['nb_bi']]
    semevs_bi_d['vm']=sem_vm_d[['nb_bi']]
    semevs_bi_d =pd.DataFrame(semevs_bi_d )
    
    """
    calculer erreur standard no pred
    """
    
        
    semevs_none_i = {}
    semevs_none_i['v0']=sem_v0_i[['nb_none']]
    semevs_none_i['v1']=sem_v1_i[['nb_none']]
    semevs_none_i['v2']=sem_v2_i[['nb_none']]
    semevs_none_i['v3']=sem_v3_i[['nb_none']]
    semevs_none_i['v4']=sem_v4_i[['nb_none']]
    semevs_none_i['v5']=sem_v5_i[['nb_none']]
    semevs_none_i['vm']=sem_vm_i[['nb_none']]
    semevs_none_i = pd.DataFrame(semevs_none_i)
    
    semevs_none_g = {}
    semevs_none_g['v0']=sem_v0_g[['nb_none']]
    semevs_none_g['v1']=sem_v1_g[['nb_none']]
    semevs_none_g['v2']=sem_v2_g[['nb_none']]
    semevs_none_g['v3']=sem_v3_g[['nb_none']]
    semevs_none_g['v4']=sem_v4_g[['nb_none']]
    semevs_none_g['v5']=sem_v5_g[['nb_none']]
    semevs_none_g['vm']=sem_vm_g[['nb_none']]
    semevs_none_g=pd.DataFrame(semevs_none_g)
    
    semevs_none_d = {}
    semevs_none_d['v0']=sem_v0_d[['nb_none']]
    semevs_none_d['v1']=sem_v1_d[['nb_none']]
    semevs_none_d['v2']=sem_v2_d[['nb_none']]
    semevs_none_d['v3']=sem_v3_d[['nb_none']]
    semevs_none_d['v4']=sem_v4_d[['nb_none']]
    semevs_none_d['v5']=sem_v5_d[['nb_none']]
    semevs_none_d['vm']=sem_vm_d[['nb_none']]
    semevs_none_d = pd.DataFrame(semevs_none_d)
    
    """
    Calculer la moyenne de nombre de prédictions de trigramme, bigramme et None
    """
    means_count_i = means_tri_i
    means_count_i = means_count_i.append(means_bi_i, ignore_index=True)
    means_count_i = means_count_i.append(means_none_i, ignore_index=True)
    means_count_i.index = ["trigramme", "bigramme", "none"]
    
    
    means_count_g = means_tri_g
    means_count_g = means_count_g.append(means_bi_g, ignore_index=True)
    means_count_g = means_count_g.append(means_none_g, ignore_index=True)
    means_count_g.index = ["trigramme", "bigramme", "none"]
    
    
    means_count_d = means_tri_d
    means_count_d = means_count_d.append(means_bi_d, ignore_index=True)
    means_count_d = means_count_d.append(means_none_d, ignore_index=True)
    means_count_d.index = ["trigramme", "bigramme", "none"]

    """
    calculer les barres d'erreurs
    """
    semevs_err_i = semevs_tri_i
    semevs_err_i = semevs_err_i.append(semevs_bi_i, ignore_index=True)
    semevs_err_i = semevs_err_i.append(semevs_none_i, ignore_index=True)
    semevs_err_i.index = ["trigramme", "bigramme", "none"]
    
    
    semevs_err_g = semevs_tri_g
    semevs_err_g = semevs_err_g.append(semevs_bi_g, ignore_index=True)
    semevs_err_g = semevs_err_g.append(semevs_none_g, ignore_index=True)
    semevs_err_g.index = ["trigramme", "bigramme", "none"]
    
    
    semevs_err_d = semevs_tri_d
    semevs_err_d = semevs_err_d.append(semevs_bi_d, ignore_index=True)
    semevs_err_d = semevs_err_d.append(semevs_none_d, ignore_index=True)
    semevs_err_d.index = ["trigramme", "bigramme", "none"]   

    nums = [1,2,3,4,5,8]  # distance entre les pas (v0, v1...)
    LABELS = ["v0", "v1", "v2", "v3", "v4", "vm"]  # étiquettes du graphique 

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)  # inisation des plots
    
    """
    Plot précision Noms
    """

    ax1.plot(nums[5:], means_pre_n_i.iloc[0][6:], color='b', marker = '.', label='_dontshow1')
    imbrique = ax1.plot(nums[0:5],means_pre_n_i.iloc[0][0:5],color='b', label='embedded')
    ax1.errorbar(nums[0:5],means_pre_n_i.iloc[0][0:5], semevs_pre_n_i.iloc[0][0:5], color='b', label='_dontshow1')
    ax1.errorbar(nums[5:],means_pre_n_i.iloc[0][6:], semevs_pre_n_i.iloc[0][6:], color='b', label='_dontshow3')

    ax1.plot(nums[5:],means_pre_n_g.iloc[0][6:], color='r', marker = '.', label='_dontshow4')
    gauche = ax1.plot(nums[0:5],means_pre_n_g.iloc[0][0:5], color='r', label='left')
    ax1.errorbar(nums[0:5],means_pre_n_g.iloc[0][0:5], semevs_pre_n_g.iloc[0][0:5], color='r', label='_dontshow5')
    ax1.errorbar(nums[5:],means_pre_n_g.iloc[0][6:], semevs_pre_n_g.iloc[0][6:], color='r', label='_dontshow6')
    
    ax1.plot(nums[5:],means_pre_n_d.iloc[0][6:],color='y', marker = '.', label='_dontshow7')
    droit = ax1.plot(nums[:5],means_pre_n_d.iloc[0][:5],color='y', label='right')
    ax1.errorbar(nums[:5],means_pre_n_d.iloc[0][:5], semevs_pre_n_d.iloc[0][:5], color='y', label='_dontshow8')
    ax1.errorbar(nums[5:],means_pre_n_d.iloc[0][6:], semevs_pre_n_d.iloc[0][6:], color='y', label='_dontshow9')
    
    ax1.plot(nums[5:],means_pre_n_b.iloc[0][6:],color='k', marker = '.', label='_dontshow7')
    baseline = ax1.plot(nums[:5],means_pre_n_b.iloc[0][:5],color='k', label='base-line')
    ax1.errorbar(nums[:5],means_pre_n_b.iloc[0][:5], semevs_pre_n_b.iloc[0][:5], color='k', label='_dontshow8')
    ax1.errorbar(nums[5:],means_pre_n_b.iloc[0][6:], semevs_pre_n_b.iloc[0][6:], color='k', label='_dontshow9')
    
    ax1.set_title('PRECISION NOUNS')
    ax1.set_xlim([0,9])
    ax1.set_ylim([0,1])

    # legende pour tout le plot
    handles, labels = ax1.get_legend_handles_labels()
        
    fig.legend([handles[0],handles[3],handles[6],handles[9]], [labels[0],labels[3],labels[6],labels[9]],loc='upper center', borderaxespad=3.0, fontsize='x-small', ncol=4)

    
    #ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='upper left',
       #ncol=2, mode="expand", borderaxespad=3.0, fontsize='x-small')
    
    """
    Plot précision Verbes
    """
    ax2.plot(nums[5:],means_pre_v_i.iloc[0][6:], color='b', marker='.')
    ax2.plot(nums[:5],means_pre_v_i.iloc[0][:5], color='b')
    ax2.errorbar(nums[:5],means_pre_v_i.iloc[0][:5], semevs_pre_v_i.iloc[0][:5],color='b')
    ax2.errorbar(nums[5:],means_pre_v_i.iloc[0][6:], semevs_pre_v_i.iloc[0][6:],color='b')
    
    ax2.plot(nums[5:],means_pre_v_g.iloc[0][6:], color='r', marker = '.')
    ax2.plot(nums[:5],means_pre_v_g.iloc[0][:5], color='r')
    ax2.errorbar(nums[5:],means_pre_v_g.iloc[0][6:], semevs_pre_v_g.iloc[0][6:], color='r')
    ax2.errorbar(nums[:5],means_pre_v_g.iloc[0][:5], semevs_pre_v_g.iloc[0][:5], color='r')
    
    ax2.plot(nums[5:],means_pre_v_d.iloc[0][6:], color='y', marker = '.')
    ax2.plot(nums[:5],means_pre_v_d.iloc[0][:5], color='y')
    ax2.errorbar(nums[5:],means_pre_v_d.iloc[0][6:], semevs_pre_v_d.iloc[0][6:], color='y')
    ax2.errorbar(nums[:5],means_pre_v_d.iloc[0][:5], semevs_pre_v_d.iloc[0][:5], color='y')
    
    ax2.plot(nums[5:],means_pre_v_b.iloc[0][6:], color='k', marker = '.')
    ax2.plot(nums[:5],means_pre_v_b.iloc[0][:5], color='k')
    ax2.errorbar(nums[5:],means_pre_v_b.iloc[0][6:], semevs_pre_v_b.iloc[0][6:], color='k')
    ax2.errorbar(nums[:5],means_pre_v_b.iloc[0][:5], semevs_pre_v_b.iloc[0][:5], color='k')
    
    ax2.set_title('PRECISION VERBS')
    ax2.set_xlim([0,9])
    ax2.set_ylim([0,1])
    
    """
    Plot rappel Noms
    """
    ax3.plot(nums[5:],means_rap_n_i.iloc[0][6:], color='b', marker = '.')
    ax3.plot(nums[:5],means_rap_n_i.iloc[0][:5], color='b')
    ax3.errorbar(nums[5:],means_rap_n_i.iloc[0][6:], semevs_rap_n_i.iloc[0][6:], color='b')
    ax3.errorbar(nums[:5],means_rap_n_i.iloc[0][:5], semevs_rap_n_i.iloc[0][:5], color='b')
    
    ax3.plot(nums[:5],means_rap_n_g.iloc[0][:5], color='r')
    ax3.plot(nums[5:],means_rap_n_g.iloc[0][6:], color='r', marker = '.')
    ax3.errorbar(nums[:5],means_rap_n_g.iloc[0][:5], semevs_rap_n_g.iloc[0][:5], color='r')
    ax3.errorbar(nums[5:],means_rap_n_g.iloc[0][6:], semevs_rap_n_g.iloc[0][6:], color='r')
    
    ax3.plot(nums[5:],means_rap_n_d.iloc[0][6:], color='y', marker = '.')
    ax3.plot(nums[:5],means_rap_n_d.iloc[0][:5], color='y')
    ax3.errorbar(nums[:5],means_rap_n_d.iloc[0][:5], semevs_rap_n_d.iloc[0][:5], color='y')
    ax3.errorbar(nums[5:],means_rap_n_d.iloc[0][6:], semevs_rap_n_d.iloc[0][6:], color='y')
    
    ax3.plot(nums[5:],means_rap_n_b.iloc[0][6:], color='k', marker = '.')
    ax3.plot(nums[:5],means_rap_n_b.iloc[0][:5], color='k')
    ax3.errorbar(nums[:5],means_rap_n_b.iloc[0][:5], semevs_rap_n_b.iloc[0][:5], color='k')
    ax3.errorbar(nums[5:],means_rap_n_b.iloc[0][6:], semevs_rap_n_b.iloc[0][6:], color='k')
    
    ax3.set_title('RECALL NOUNS')
    ax3.set_xlim([0,9])
    ax3.set_ylim([0,1])

    
    """
    Plot rappel Verbes
    """
    ax4.plot(nums[5:],means_rap_v_i.iloc[0][6:], color='b', marker = '.')
    ax4.plot(nums[:5],means_rap_v_i.iloc[0][:5], color='b')
    ax4.errorbar(nums[5:],means_rap_v_i.iloc[0][6:], semevs_rap_v_i.iloc[0][6:], color='b')
    ax4.errorbar(nums[:5],means_rap_v_i.iloc[0][:5], semevs_rap_v_i.iloc[0][:5], color='b')
    
    ax4.plot(nums[5:],means_rap_v_g.iloc[0][6:], color='r', marker = '.')
    ax4.plot(nums[:5],means_rap_v_g.iloc[0][:5], color='r')
    ax4.errorbar(nums[:5],means_rap_v_g.iloc[0][:5], semevs_rap_v_g.iloc[0][:5], color='r')
    ax4.errorbar(nums[5:],means_rap_v_g.iloc[0][6:], semevs_rap_v_g.iloc[0][6:], color='r')
    
    ax4.plot(nums[5:],means_rap_v_d.iloc[0][6:], color='y', marker = '.')
    ax4.plot(nums[:5],means_rap_v_d.iloc[0][:5], color='y')
    ax4.errorbar(nums[5:],means_rap_v_d.iloc[0][6:], semevs_rap_v_d.iloc[0][6:], color='y')
    ax4.errorbar(nums[:5],means_rap_v_d.iloc[0][:5], semevs_rap_v_d.iloc[0][:5], color='y')
    
    ax4.plot(nums[5:],means_rap_v_b.iloc[0][6:], color='k', marker = '.')
    ax4.plot(nums[:5],means_rap_v_b.iloc[0][:5], color='k')
    ax4.errorbar(nums[5:],means_rap_v_b.iloc[0][6:], semevs_rap_v_b.iloc[0][6:], color='k')
    ax4.errorbar(nums[:5],means_rap_v_b.iloc[0][:5], semevs_rap_v_b.iloc[0][:5], color='k')
    
    ax4.set_title('RECALL VERBS')
    ax4.set_xlim([0,9])
    ax4.set_ylim([0,1])

    # étiquetter les axes
    plt.setp(((ax1, ax2), (ax3, ax4)), xticks=nums, xticklabels=LABELS)
    plt.xticks(nums, LABELS)
    plt.tight_layout(pad=4.0, w_pad=2.0, h_pad=2.0)  #  mise en page
    plt.savefig("resultats/resultats.png", dpi=500) # sauvegarde du graph
    #plt.show()  # montrer le plot à l'écran
    
    plt.close()
    
    means_count_i = means_count_i.transpose()
    means_count_g = means_count_g.transpose()
    means_count_d = means_count_d.transpose()
    
    semevs_count_i = semevs_err_i.transpose()
    semevs_count_g = semevs_err_g.transpose()
    semevs_count_d = semevs_err_d.transpose()
    
    """
    Faire un plot de combien de fois les modèles ont prédits avec un trigramme, un bigramme ou rien (None)
    """
    
    fig, ax = plt.subplots()
    
    imb3 = ax.bar([1,6,11,16,21,26,31], means_count_i['none'],color='b', yerr=semevs_count_i['none'])
    imb2 = ax.bar([1,6,11,16,21,26,31], means_count_i['bigramme'], color='g', bottom=means_count_i['none'], yerr=semevs_count_i['bigramme'])
    imb1 = ax.bar([1,6,11,16,21,26,31], means_count_i['trigramme'], color='c', bottom=(means_count_i['bigramme']+means_count_i['none']), yerr=semevs_count_i['trigramme'])
    
    gau3 = ax.bar([2,7,12,17,22,27,32], means_count_g['none'],color='r', yerr=semevs_count_g['none'])
    gau2 = ax.bar([2,7,12,17,22,27,32], means_count_g['bigramme'],color='violet', bottom=means_count_g['none'], yerr=semevs_count_g['bigramme'])
    gau1 = ax.bar([2,7,12,17,22,27,32], means_count_g['trigramme'],color='pink', bottom=(means_count_g['bigramme']+means_count_g['none']), yerr=semevs_count_g['trigramme'])
    
    dr3 = ax.bar([3,8,13,18,23,28,33], means_count_d['none'],color='orange', yerr=semevs_count_d['none'])
    dr2 = ax.bar([3,8,13,18,23,28,33], means_count_d['bigramme'],color='y', bottom=means_count_d['none'], yerr=semevs_count_d['bigramme'])
    dr1 = ax.bar([3,8,13,18,23,28,33], means_count_d['trigramme'],color='w', bottom=(means_count_d['bigramme']+means_count_d['none']), yerr=semevs_count_d['trigramme'])
    
       
     
    #ax.legend( (imb1, imb2, imb3, gau1,gau2,gau3, dr1, dr2, dr3), ('n=3 I', 'n=2 I', 'None I', 'n=3 G', 'n=2 G', 'None G', 'n=3 D', 'n=2 D', 'None D')
    #            , bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., labelspacing=0.2 )
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.subplots_adjust(right=0.7)
    plt.subplots_adjust(top=0.9)
    plt.xticks([2,7,12,17,22,27,32], ["V0", "V1", "V2", "V3", "V4", "V5", "Vm"])
    plt.title("Nombre de prédictions par n-gramme \n pour les modèles imbriqué(I), gauche(G) et droit(D)", size='small', y=1.00)
    plt.savefig("resultats/nb_preds.png", dpi=1000) # sauvegarde du graph
    #plt.show()  # montrer le plot à l'écran
    
    
"""
Argument du programme: le chemin vers le dossier avec les résultats des résultats des modèles."
"""
parser = argparse.ArgumentParser()
parser.add_argument("dir_results", help="le chemin vers le dossier avec les résultats des modèles")
args  = parser.parse_args()
dir_results = args.dir_results


get_plot(dir_results+"modele_imbrique_v0.txt", dir_results + 
         "modele_imbrique_v1.txt",dir_results+"modele_imbrique_v2.txt", 
         dir_results+"modele_imbrique_v3.txt",
         dir_results+"modele_imbrique_v4.txt",
         dir_results+"modele_imbrique_v5.txt",
         dir_results+"modele_imbrique_vm.txt",
         
         dir_results+"modele_gauche_v0.txt", dir_results + 
         "modele_gauche_v1.txt",dir_results+"modele_gauche_v2.txt", 
         dir_results+"modele_gauche_v3.txt",
         dir_results+"modele_gauche_v4.txt",
         dir_results+"modele_gauche_v5.txt",
         dir_results+"modele_gauche_vm.txt",
         
         dir_results+"modele_droit_v0.txt", dir_results + 
         "modele_droit_v1.txt",dir_results+"modele_droit_v2.txt", 
         dir_results+"modele_droit_v3.txt", 
         dir_results+"modele_droit_v4.txt", 
         dir_results+"modele_droit_v5.txt", 
         dir_results+"modele_droit_vm.txt",
         
         dir_results+"modele_baseline_v0.txt", dir_results + 
         "modele_baseline_v1.txt",dir_results+"modele_baseline_v2.txt", 
         dir_results+"modele_baseline_v3.txt", 
         dir_results+"modele_baseline_v4.txt", 
         dir_results+"modele_baseline_v5.txt", 
         dir_results+"modele_baseline_vm.txt")
