#!/usr/bin/env python # -*- coding: utf-8 -*-

import os, argparse

"""
Ce programme sert à corriger le corpus de CHILDES annoté par la ligne de MOR dans CLAN.
Le problème est que trop de tokens qui ne sont pas un Nom sont annoté comme "n". 
Le but du programme est de corriger ces items.
"""

def learn_new_tags(fichier):
    """
    Prend en paramètre un fichier avec la forme suivante:
    
    pour    prep
    marche    v
    
    Le fichier donne la liste de mots qu'il faudra retagguer avec leur tag plus approprié.
    La fonction importe ces informations dans le programme.
    @param fichier: le fichier qui contient les mots à retaguer avec leur catégorie syntaxique.
    """
    tagging = {}
    new_tags = open(fichier, 'r', encoding='utf-8')
    line = new_tags.readline()
    while line!='':
        word_tag = line.split('\n')[0]
        list = word_tag.split("\t")
        word = list[0]
        tag = list [1]
        tagging[word] = tag
        line = new_tags.readline()
    return tagging

  
def rewrite_corpus(dir_in, dir_out, new_tags):
    """
    Fonction qui sert à produire une version du corpus corrigé
    @param dir_in: le répertoire dans lequel le corpus se trouve
    @param dir_out: le répertoire dans lequel le corpus corrigé doit être écrit
    @new_tags: la structure produite par la fonction "learn_new_tags" qui indique où il faut effectuer des corrections.
    """
    nb_changements = 0
    i = 1
    for subdir, dirs, files in os.walk(dir_in):
            for file in files:
                fic = open(dir_in+file,'r', encoding='utf-8')
                new_file = open(dir_out+str(i)+".txt", 'w', encoding='utf-8') 
                line = fic.readline()
                while line != '':
                    toks= line.split('\t')
                    if line != "\r\n" and line !="\n":
                        if toks[2] in new_tags and toks[3] == "n":
                            toks[3] = new_tags[toks[2]]
                            nb_changements = nb_changements + 1
                    toks = "\t".join(toks)
                    new_file.write(str(toks))
                    line = fic.readline()
                i = i +1
                fic.close()
                new_file.close()
    print ("Nombre de corrections effectué :", nb_changements)
       
"""
Les arguments du programme: le chemin vers le corpus non-corrigé et le chemin vers le dossier dans lequel le programme écrira
le corpus corrigé.
"""          
parser = argparse.ArgumentParser()
parser.add_argument("corpus", help="Cet argument est le chemin vers le corpus non-corrigé")
parser.add_argument("corrected_corpus", help="Cet argument est le chemin vers le dossier où sera produit le corpus corrigé")
args  = parser.parse_args()
corpus = args.corpus
corpus_corrige = args.corrected_corpus


new_tags = learn_new_tags("retagged_nouns_version_papier.csv")
dir_out = corpus_corrige     
dir_in = corpus

rewrite_corpus(dir_in,dir_out,new_tags)

                    
