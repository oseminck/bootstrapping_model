#!/usr/bin/env python # -*- coding: utf-8 -*-
import copy, argparse
import pickle
from corpus import Corpus 
from nltk.metrics.association import TrigramAssocMeasures
import numpy as np
from call_my_corpus import utterances


class ModeleContextesImbriques():
    """
    Le modèle des contextes imbriqués. Pour un mot "cible" (les mots cibles sont des mots avec une basse fréquence dans le corpus)
    le modèle considéra le token avant et après ce mot cible. 
    """
    
    def __init__(self, graine_sem, test_vocab, train, test):
        self.train = train  # le corpus d'entraînement
        self.graine_sem = graine_sem  # la liste des lemmes de la graine sémantique
        self.trigrams = {}  # lors de la phase d'entraîntement, ce dictionnaire sera rempli avec les trigrams du corpus
        self.bigrams = {}  # dictionnaire avec les bigrams du corpus pour le repli
        self.test = test  # le corpus de test
        self.test_vocab = test_vocab  # liste avec les mots cibles, donc les mots pour lesquels lors de la phase de test on va prédire la catégorie
        self.misses_n = 0  # nombre de faux négatifs pour la catégorie Nom
        self.misses_v = 0  # nombre de faux négatifs pour la catégorie Verbe
        self.bien_pred_n = 0  # nombre de vrais positifs pour la catégorie Nom
        self.bien_pred_v = 0  # nombre de vrais postifs pour la catégorie Verbe 
        self.false_allarms_n = 0  # nombre de faux positifs pour la catégorie Nom
        self.false_allarms_v = 0  # nombre de faux positifs pour la catégorie Verbe
        self.relying_on_trigram = 0  # nombre de fois qu'on a basée la prédiction sur un trigram
        self.relying_on_bigram = 0  # nombre de fois qu'on s'est replié sur un bigram pour faire la prédiction
        self.cannot_find = 0  # nombre de fois qu'aucune prédiction n'est faite, faute de trigram et de bigrams connus dans le contexte
        self.errors = {"fa_n": {}, "fa_v": {}, "miss_n":{}, "miss_v":{}}  # structure pour analyser les erreurs
        self.count_trigrammes={}
        voca = open("voca", 'rb')  # le vocabulaire du corpus, on en a besoin pour effectuer l'analyse des erreurs.
        self.voca = pickle.load(voca)
        voca.close()
    
    
    def projection(self, ngram, position):  
        """
        On remplace tous les mots de la graine sémantique par leur catégorie morpho-syntaxique.
        @param ngram : le ngram à projeter
        @param position : la position cible du trigram
        """
        ngr = copy.deepcopy(ngram) 
        if ngr[position][2] in self.graine_sem:
            if ngr[position][3] in ["n", "n:let"]:
                ngr[position][1] = "n"
            elif ngr[position][3] in ["v:mdl", "v:mdllex", "v:pos", "v"]:
                ngr[position][1] = "v"
        return ngr
         
    
    def count_trigrams(self, trigram, val):
        """
        Fonction utilisée pour ajouter un trigram aux n-grams connus lors de la phase d'entraînement.
        @param trigram: le trigram à stocker
        @param val: le mot qui se trouve dans la position cible du trigram
        """
        if trigram in self.trigrams:
            if val in self.trigrams[trigram]:
                self.trigrams[trigram][val] = self.trigrams[trigram][val] + 1
            else:
                self.trigrams[trigram][val]=1
        else:
            self.trigrams[trigram] = {val:1}
        
        
    def count_bigrams(self, bigram, val):
        """
        Fonction utilisée pour ajouter un bigram aux n-grams connus lors de la phase d'entraînement.
        @param bigram: le bigram à stocker.
        @param val: le mot qui se trouve dans la position cible du bigram.
        """
        if bigram in self.bigrams:
            if val in self.bigrams[bigram]:
                self.bigrams[bigram][val] = self.bigrams[bigram][val] + 1
            else:
                self.bigrams[bigram][val]=1
        else:
            self.bigrams[bigram] = {val:1}
                      
     
    def get_ngrams(self):
        """
        Cette méthode fait le comptage des différents trigrams et bigrams dans un énoncé passé en paramètre. 
        """
        for utterance in self.train:
            if utterance[len(utterance)-1][3] =="Punc":
                utterance = utterance[:len(utterance)-1]
            utterance.append(["}","}","}","}","}"])  # frontière
            utterance.insert(0,["{","{","{","{","{"])  # frontière
            trigram = []
            for i in range(len(utterance)-2):
                for j in range(0,3):
                    trigram.append(utterance[i+j][1])
                trigram = self.projection(utterance[i:i+3], 1)
                val = copy.deepcopy(trigram[1][1])
                trigram = copy.deepcopy(trigram[0][1]+" "+trigram[2][1])
                self.count_trigrams(trigram, val)
                trigram = []
            bigram = []
            for i in range(len(utterance)-2):
                for j in range(0,2):
                    bigram.append(utterance[i+j][1])
                bigram = copy.deepcopy(self.projection(utterance[i:i+2],1))
                val = bigram[1][1]
                bigram = str(bigram[0][1])
                self.count_bigrams(bigram, val)
                bigram = []    

    
    def do_the_test(self):
        """
        Méthode qui permet de tester le modèle.
        Elle parcourt le corpus de test et fait des prédictions sur les mots avec une fréquence inférière à 0.0005 du corpus.
        """
        for i in range(len(self.test)):
            for j in range(len(self.test[i])):
                if self.test[i][j][1] in self.test_vocab and self.test[i][j][3] !="?" and self.test[i][j][3] !='co':
                    self.make_prediction(self.test[i], j)


    def make_prediction(self, utterance, indice):
        """
        Méthode qui fait une prédiction pour un mot cible dans un certain énoncé.
        @param utterance: un énoncé dans lequel il y a un mot pour lequel il faut faire une prédiction.
        @param indice: la position du mot à prédire dans l'énoncée.
        """
        if utterance[len(utterance)-1][3] =="Punc":
            utterance = utterance[:len(utterance)-1]
        utterance.append(["}","}","}","}","}"]) # fronitère 
        utterance.insert(0,["{","{","{","{","{"]) # frontière
        trigram = str(utterance[indice][1])+" "+str(utterance[indice+2][1])
        ans = ""
        if trigram in self.trigrams and trigram != "{ }":
            self.relying_on_trigram = self.relying_on_trigram +1
            ans = self.get_max_for_trigram(trigram)
            self.evaluation(ans, utterance[indice+1][3])
        else:
            bigram = str(utterance[indice][1])
            if bigram in self.bigrams and bigram != "{":
                self.relying_on_bigram = self.relying_on_bigram + 1
                ans = self.get_max_for_bigram(bigram)
                self.evaluation(ans, utterance[indice+1][3])
            elif bigram != "{":
                self.cannot_find = self.cannot_find + 1
        if trigram != "{ }":
            self.count_used_trigrams(trigram, ans, utterance[indice+1][3])
                
    
    def count_used_trigrams(self, trigram, ans, real_ans):
        """
        Permet de trouver quels trigrams ont été utlisés lors de la prédiction. 
        Les comptages suivants sont faits:
        - nombre de fois que chaque trigram a été utlisé lors de la prédiction.
        - nombre de fois que chaque trigram a été utlisé pour un cible Nom
        - nombre de fois que chaque trigram a été utlisé pour un cible Verbe
        - la réponse du modèle quand le trigram est utilisé
        @param trigram : le trigram pour lequel les comptes sont mis à jour
        @param ans : la réponse que le modèle donne avec ce trigram
        @param real_ans : la catégorie que le trigram devrait prédire
        """
        if trigram in self.count_trigrammes:
            self.count_trigrammes[trigram]['ut'] = self.count_trigrammes[trigram]['ut'] + 1
            if real_ans == 'n':
                self.count_trigrammes[trigram]['n'] = self.count_trigrammes[trigram]['n'] + 1
            elif real_ans == 'v':
                self.count_trigrammes[trigram]['v'] = self.count_trigrammes[trigram]['v'] + 1
        else:
            self.count_trigrammes[trigram] = {'ut':1, 'n':0, 'v':0, 'rep':ans}
            if real_ans == 'n':
                self.count_trigrammes[trigram]['n'] = self.count_trigrammes[trigram]['n'] + 1
            elif real_ans == 'v':
                self.count_trigrammes[trigram]['v'] = self.count_trigrammes[trigram]['v'] + 1


    def evaluation(self, ans, real_ans): 
            """
            Fonction qui permet de faire l'analyse des erreurs. 
            Les erreus sont stockés dans une structure de dictionnaire self.errors. 
            Il y a 4 sous-dictionnaires: un pour les fausses allarmes des noms, un pour 
            les fausses allarmes des verbes, un pour les noms manqués et un pour les verbes manqués.
            Pour les fausses allarmes on compte combien de fois un élément d'une catégorie autre que 
            la bonne catégorie (nom ou verbe) a été indiqué comme nom ou verbe par le modèle.
            Pour les manqués, la fonction inspectera la nature du mot prédit. Si par exemple le programme
            aurait dû prédire un nom, mais au lieu de cela il prédit "fille", cela sera compté comme un n.
            Si, au contraire, le programme devait prédire nom, mais a prédit "souvent", dans la structure pour les 
            noms manqués le comptage de la catégorie adverbe sera augmenté.
            @param ans: la réponse donné par le modèle.
            @param real_ans: la vraie catégorie morpho-syntaxique du cible.
            """
            if ans == "n" and real_ans in ["n:prop", "n:let", "n"]:
                self.bien_pred_n = self.bien_pred_n + 1
            elif ans == "v" and real_ans in ["v:mdl", "v:mdllex", "v:pos", "v"]:
                self.bien_pred_v = self.bien_pred_v + 1
            elif ans == "n":
                self.false_allarms_n = self.false_allarms_n + 1
                if real_ans in self.errors["fa_n"]:
                    self.errors["fa_n"][real_ans] = self.errors["fa_n"][real_ans] + 1
                else:
                    self.errors["fa_n"][real_ans] = 1
            elif ans == "v":
                self.false_allarms_v = self.false_allarms_v + 1
                if real_ans in self.errors["fa_v"]:
                    self.errors["fa_v"][real_ans] = self.errors["fa_v"][real_ans] + 1
                else:
                    self.errors["fa_v"][real_ans] = 1
            if real_ans in ["n", "n:let"] and ans !='n':
                self.misses_n = self.misses_n + 1
                if "n" in self.voca[ans] or "n:let" in self.voca[ans] or "n:prop" in self.voca[ans]:
                    if "n" in self.errors["miss_n"]:
                        self.errors["miss_n"]["n"] = self.errors["miss_n"]["n"] + 1
                    else:
                        self.errors["miss_n"]["n"] =1
                elif ans =='v':
                    if "V" in self.errors["miss_n"]:
                        self.errors["miss_n"]["V"] = self.errors["miss_n"]["V"] +1
                    else:
                        self.errors["miss_n"]['V'] = 1

                else:
                    max_pos = self.get_max_pos(ans)
                    if max_pos in self.errors["miss_n"]:
                        self.errors["miss_n"][max_pos] = self.errors["miss_n"][max_pos] + 1
                    else:
                        self.errors["miss_n"][max_pos] = 1
            if real_ans in ["v:mdl", "v:mdllex", "v:pos", "v"] and ans != 'v':
                self.misses_v = self.misses_v +1
                if "v:mdl" in self.voca[ans] or "v:mdllex" in self.voca[ans] or "v:pos" in self.voca[ans] or "v" in self.voca[ans]:
                    if "v" in self.errors["miss_v"]:
                        self.errors["miss_v"]["v"] = self.errors["miss_v"]["v"] + 1
                    else:
                        self.errors["miss_v"]["v"] =1
                        
                elif ans =='n':
                    if "N" in self.errors["miss_v"]:
                        self.errors["miss_v"]["N"] = self.errors["miss_v"]["N"] +1
                    else:
                        self.errors["miss_v"]['N'] = 1
                else:
                    max_pos = self.get_max_pos(ans)
                    if max_pos in self.errors["miss_v"]:
                        self.errors["miss_v"][max_pos] = self.errors["miss_v"][max_pos] + 1
                    else:
                        self.errors["miss_v"][max_pos] = 1



    def get_neat_error_results(self, errors,nb_errors, file, i):
        """
        Méthode qui sert à écrire l'analyse des erreurs dans un fichier sous forme de tableau.
        @param errors: une structure de dictionnaire dans laquelle on indique quelle catégorie a été faussement prédite.
        @param nb_errors: le nombre total des errors d'un certain type (fausses allarmes N, faussees allarmes V, manqués N, manqués V)
        @param file: fichier dans lequel les analyses seront écrites.
        @param i: nombre du k-fold.
        """
        new_dic_errors = {"pro":0, "n":0, "v":0, "co":0, "adv":0, "prep":0, "det":0, "conj":0, "adj":0, "?":0, "autre":0, "N":0, "V":0}
        keys = new_dic_errors.keys()
        keys_str = ""  # noms des colonnes dans le fichier
        for key in keys:
            keys_str = keys_str + key + "\t"
        keys_str = keys_str + "\n"
        if i ==0:
            file.write("k-fold\ttot\t"+keys_str)
        for pos in errors:
            cat = pos.split(":")[0]
            if cat in new_dic_errors:
                new_dic_errors[cat] = new_dic_errors[cat] + errors[pos]
            else:
                new_dic_errors["autre"]= new_dic_errors["autre"] + errors[pos]
        to_string = ""
        for key in keys:
            to_string = to_string + str(new_dic_errors[key])+"\t"
        to_string = to_string  + "\n"
        file.write(str(i)+"\t"+str(nb_errors)+"\t"+to_string)
        
    
    def get_max_pos(self,ans):
        """
        Fonction auxiliaire de la fonction evaluation.
        Elle sert à dire quelle est (fort probablement) la catégorie du mot prédit par le modèle.
        Donc si le modèle prédit "vite" au lieu de "n", cette fonction va retourner "adv".
        @param ans: la réponse donnée par le système.
        """
        max = 0
        max_key = ""
        for key in self.voca[ans].keys():
            if self.voca[ans][key] > max:
                max = self.voca[ans][key]
                max_key = key
        return max_key  
    
    
    def get_max_for_trigram(self,trigram):
        """
        Méthode qui cherche la catégorie morpho-syntaxique rencontrée le plus souvent dans le contexte (le trigram).
        @param trigram: le trigram en question.
        """
        max = 0
        ans_max = ""
        for val in self.trigrams[trigram]:
            if self.trigrams[trigram][val]> max:
                max = self.trigrams[trigram][val]
                ans_max = val
        return ans_max
    
    
    def get_max_for_bigram(self, bigram):
        """
        Méthode qui cherche la catégorie morpho-syntaxique rencontrée le plus souvent dans le contexte (le bigram).
        @param: le bigram en question.
        """
        max = 0
        ans_max = ""
        for val in self.bigrams[bigram]:
            if self.bigrams[bigram][val]> max:
                max = self.bigrams[bigram][val]
                ans_max = val
        return ans_max
    


class ModeleContextesGauches(ModeleContextesImbriques):
    """
    Classe qui hérite de la classe ModeleContextesImbriques, mais deux méthodes sont différentes pour prendre un trigram qui 
    représente le contexte gauche d'un mot cible. C'est-à-dire les deux mots avant le mot cible.
    """
    
    def get_ngrams(self):
        """
        Methode qui trouve les trigrammes pour le modèle du contexte gauche.
        """
        for utterance in self.train:
            if utterance[len(utterance)-1][3] =="Punc":
                utterance = utterance[:len(utterance)-2]
            utterance.insert(0,["{","{","{","{","{"])
            utterance.insert(0,["{","{","{","{","{"])
            trigram = []
            for i in range(len(utterance)-2):
                for j in range(0,3):
                    trigram.append(utterance[i+j][1])
                trigram = self.projection(utterance[i:i+3], 2)
                val = copy.deepcopy(trigram[2][1])
                trigram = copy.deepcopy(trigram[0][1]+" "+trigram[1][1])
                self.count_trigrams(trigram, val)
                trigram = []
            bigram = []
            for i in range(len(utterance)-1):
                for j in range(0,2):
                    bigram.append(utterance[i+j][1])
                bigram = copy.deepcopy(self.projection(utterance[i:i+2],1))
                val = bigram[1][1]
                bigram = str(bigram[0][1])
                self.count_bigrams(bigram, val)
                bigram = []    


    def make_prediction(self, utterance, indice):
        """
        Modèle qui fait la prédiction pour le modèle des contextes gauches.
        @param utterance: l'énoncée dans laquelle il se trouve un mot pour lequel on voudrait faire une prédiction.
        @indice: la position dans l'énoncée où se trouve le mot à prédire.
        """
        if utterance[len(utterance)-1][3] =="Punc":
            utterance = utterance[:len(utterance)-1]
        utterance.insert(0,["{","{","{","{","{"])
        utterance.insert(0,["{","{","{","{","{"])
        trigram = str(utterance[indice][1])+" "+str(utterance[indice+1][1])
        ans = ""
        if trigram in self.trigrams and trigram != "{ {":
            self.relying_on_trigram = self.relying_on_trigram +1
            ans = self.get_max_for_trigram(trigram)
            self.evaluation(ans, utterance[indice+2][3])
        else:
            bigram = str(utterance[indice+1][1])
            if bigram in self.bigrams and bigram !="{":
                self.relying_on_bigram = self.relying_on_bigram + 1
                ans = self.get_max_for_bigram(bigram)
                self.evaluation(ans, utterance[indice+2][3])
            elif bigram !="{":
                self.cannot_find = self.cannot_find + 1
        if trigram != "{ {":
            self.count_used_trigrams(trigram, ans, utterance[indice+2][3])


class ModeleContextesDroits(ModeleContextesImbriques):
    """
    Classe qui hérite de la classe ModeleContextesImbriques, mais deux méthodes sont différentes pour prendre un trigram qui 
    représente le contexte droit d'un mot cible. C'est-à-dire les deux mots après le mot cible.
    """
    
     
    def get_ngrams(self):
        """
        Méthode qui trouve les trigrammes pour le modèle du contexte droit.
        """
        for utterance in self.train:
            if utterance[len(utterance)-1][3] =="Punc":
                utterance = utterance[:len(utterance)-2]
            utterance.append(["}","}","}","}","}"])
            utterance.append(["}","}","}","}","}"])
            trigram = []
            for i in range(len(utterance)-2):
                for j in range(0,3):
                    trigram.append(utterance[i+j][1])
                trigram = self.projection(utterance[i:i+3], 0)
                val = copy.deepcopy(trigram[0][1])
                trigram = copy.deepcopy(trigram[1][1]+" "+trigram[2][1])
                self.count_trigrams(trigram, val)
                trigram = []
            bigram = []
            for i in range(len(utterance)-1):
                for j in range(0,2):
                    bigram.append(utterance[i+j][1])
                bigram = copy.deepcopy(self.projection(utterance[i:i+2],0))
                val = bigram[0][1]
                bigram = str(bigram[1][1])
                self.count_bigrams(bigram, val)
                bigram = []    


    def make_prediction(self, utterance, indice):
        """
        Méthode qui fait la prédiction pour le modèle du contexte droit.
        @param utterance: l'énoncée dans laquelle il se trouve un mot pour lequel on voudrait faire une prédiction.
        @indice: la position dans l'énoncée où se trouve le mot à prédire.
        """
        if utterance[len(utterance)-1][3] =="Punc":
            utterance = utterance[:len(utterance)-1]
        utterance.append(["}","}","}","}","}"])
        utterance.append(["}","}","}","}","}"])
        trigram = str(utterance[indice+1][1])+" "+str(utterance[indice+2][1])
        ans = ""
        if trigram in self.trigrams and trigram !="} }":
            self.relying_on_trigram = self.relying_on_trigram +1
            ans = self.get_max_for_trigram(trigram)
            self.evaluation(ans, utterance[indice][3])
        else:
            bigram = str(utterance[indice+1][1])
            if bigram in self.bigrams and bigram != "}":
                self.relying_on_bigram = self.relying_on_bigram + 1
                ans = self.get_max_for_bigram(bigram)
                self.evaluation(ans, utterance[indice][3])
            elif bigram != "}":
                self.cannot_find = self.cannot_find + 1
        if trigram !="} }":
            self.count_used_trigrams(trigram, ans, utterance[indice][3])    


        
class Modele_Imbrique_Vm(ModeleContextesImbriques):
    """
    Modèle qui hérite de la classe ModeleContextesImbriques.
    La différence pour ce modèle que tous les noms et les verbes du corpus sont projetés.
    Donc la fonction projection est redéfinie.
    """
    
    def projection(self, ngram, position):   
        """
        On remplace tous les mots de la graine sémantique par leur catégorie morpho-syntaxique.
        @param ngram : le ngram à projeter
        @param position : la position cible du trigram
        """
        ngr = copy.deepcopy(ngram) 
        if ngr[position][3] in ["n", "n:let"]:
            ngr[position][1] = "n"
        elif ngr[position][3] in ["v:mdl",  "v:mdllex", "v:pos", "v"]:
            ngr[position][1] = "v"
        return ngr
    
    
class Modele_Gauche_Vm(ModeleContextesGauches):
    """
    Modèle qui hérite de la classe ModeleContextesGauches.
    La différence pour ce modèle que tous les noms et les verbes du corpus sont projectés.
    Donc la fonction projection est redéfinie.
    """
    
    
    def projection(self, ngram, position):   
        """
        On remplace tous les mots de la graine sémantique par leur catégorie morpho-syntaxique.
        @param ngram : le ngram à projeter
        @param position : la position cible du trigram
        """
        ngr = copy.deepcopy(ngram) 
        if ngr[position][3] in ["n", "n:let"]:
            ngr[position][1] = "n"
        elif ngr[position][3] in ["v:mdl", "v:mdllex", "v:pos", "v"]:
            ngr[position][1] = "v"
        return ngr
    
    
class Modele_Droit_Vm(ModeleContextesDroits):
    """
    Modèle qui hérite de la classe ModeleContextesDroits.
    La différence pour ce modèle que tous les noms et les verbes du corpus sont projectés.
    Donc la fonction projection est redéfinie.
    """
    
    
    def projection(self, ngram, position):
        """
        On remplace tous les mots de la graine sémantique par leur catégorie morpho-syntaxique.
        @param ngram : le ngram à projeter
        @param position : la position cible du trigram
        """
        ngr = copy.deepcopy(ngram) 
        if ngr[position][3] in ["n", "n:let"]:
            ngr[position][1] = "n"
        elif ngr[position][3] in ["v:mdl", "v:mdllex", "v:pos", "v"]:
            ngr[position][1] = "v"
        return ngr
    

class Modele_Baseline(ModeleContextesImbriques):
    """
    Modèle qui hérite de la classe ModeleContextesImbriques.
    Ce modèle prédit la catégorie 'nom', 'verbe' ou 'autre' sans se baser sur le contexte.
    Le modèle regarde quel pourcentage des occurrences des noms et des verbes est couvert par la graine sémantique. 
    Ces pourcentages sont utilisés pour faire un tir aléatoire pondéré pour faire les préditions. 
    """
    def __init__(self, graine_sem, test_vocab, train, test):
        self.train = train  # le corpus d'entraînement
        self.graine_sem = graine_sem  # la liste des lemmes de la graine sémantique
        self.trigrams = {}  # lors de la phase d'entraîntement, ce dictionnaire sera rempli avec les trigrams du corpus
        self.bigrams = {}  # dictionnaire avec les bigrams du corpus pour le repli
        self.test = test  # le corpus de test
        self.coverage = {'n': 0, 'v': 0, 'other': 0}
        self.test_vocab = test_vocab  # liste avec les mots cibles, donc les mots pour lesquels lors de la phase de test on va prédire la catégorie
        self.misses_n = 0  # nombre de faux négatifs pour la catégorie Nom
        self.misses_v = 0  # nombre de faux négatifs pour la catégorie Verbe
        self.bien_pred_n = 0  # nombre de vrais positifs pour la catégorie Nom
        self.bien_pred_v = 0  # nombre de vrais postifs pour la catégorie Verbe 
        self.false_allarms_n = 0  # nombre de faux positifs pour la catégorie Nom
        self.false_allarms_v = 0  # nombre de faux positifs pour la catégorie Verbe
        self.relying_on_trigram = 0  # nombre de fois qu'on a basée la prédiction sur un trigram
        self.relying_on_bigram = 0  # nombre de fois qu'on s'est replié sur un bigram pour faire la prédiction
        self.cannot_find = 0  # nombre de fois qu'aucune prédiction n'est faite, faute de trigram et de bigrams connus dans le contexte
        self.errors = {"fa_n": {}, "fa_v": {}, "miss_n":{}, "miss_v":{}}  # structure pour analyser les erreurs
        self.count_trigrammes={}
        voca = open("voca", 'rb')  # le vocabulaire du corpus, on en a besoin pour effectuer l'analyse des erreurs.
        self.voca = pickle.load(voca)
        voca.close()
    
    
    def get_pourc_n(self):
        """
        donne la couverture des noms dans le corpus selon les différentes graines sémantiques.
        """
        return float(self.coverage['n'])/float(self.coverage['total'])
#         if len(self.graine_sem) == 6:
#             return 0.0329995131789
#         if len(self.graine_sem) == 12:
#             return 0.0590444398081
#         if len(self.graine_sem) == 24:
#             return 0.0980248974198
#         if len(self.graine_sem) == 48:
#             return 0.15696501843
#         if len(self.graine_sem) == 96:
#             return 0.242436887127
#         if len(self.graine_sem) == 192:
#             return 0.35061548091
#         else:
#             print "pas la bonne graine sémantique"
#             raw_input()
            
            
    def get_pourc_v(self):
        """
        donne la couverture des verbes dans le corpus selon les différentes graines sémantiques.
        """
        pourc_v =  float(self.coverage['v'])/float(self.coverage['total'])
        return pourc_v
    

#         if len(self.graine_sem) == 6:
#             return 0.0315077296583
#         if len(self.graine_sem) == 12:
#             return 0.0501624477846
#         if len(self.graine_sem) == 24:
#             return 0.0761362419222
#         if len(self.graine_sem) == 48:
#             return 0.109054232568
#         if len(self.graine_sem) == 96:
#             return 0.14457852833
#         if len(self.graine_sem) == 192:
#             return 0.14457852833
#         else:
#             print "pas la bonne graine sémantique"
#             raw_input()
            
    
    def get_ngrams(self):
        """
        Cette méthode fait le comptage des différents trigrams et bigrams dans un énoncé passé en paramètre. 
        """ 
        self.coverage = {'n': 0, 'v': 0, 'other': 0}
        for utterance in self.train:
            if utterance[len(utterance)-1][3] =="Punc":
                utterance = utterance[:len(utterance)-1]
            for i in range(len(utterance)):
                if utterance[i][3] in ["n:prop", "n:let", "n"] and utterance[i][2] in self.graine_sem:
                    self.coverage['n'] += 1
                elif utterance[i][3] in ["v:mdl", "v:mdllex", "v:pos", "v"] and utterance[i][2] in self.graine_sem:
                    self.coverage['v'] += 1
                else: 
                    self.coverage['other'] += 1
        print(self.coverage)
        self.coverage['total'] = self.coverage['n'] + self.coverage['v'] + self.coverage['other']
        
    
    def make_prediction(self, utterance, indice):
        """
        Fonction qui donne une prédiction de la catégorie sans se baser sur le contexte. 
        Un tir aléatoire est fait qui est pondéré pour 'nom', 'verbe' et 'autre' selon la couverture de la 
        graine sémantique. 
        @param utterance : l'énoncé sous forme de liste avec un mot à prédire dedans
        @param indice : la position dans l'utterance du mot à prédire
        """
        pourc_n = self.get_pourc_n()
        pourc_v = self.get_pourc_v()
        ans = np.random.choice(["n", "v", utterance[indice][1]], 1, p=[pourc_n,pourc_v, (1.0-pourc_n-pourc_v)])
        self.evaluation(ans[0], utterance[indice][3])


class Modele_Baseline_Vm(Modele_Baseline): 
            
         
    def get_ngrams(self):
        """
        Cette méthode fait le comptage des différents trigrams et bigrams dans un énoncé passé en paramètre. 
        """ 
        self.coverage = {'n': 0, 'v': 0, 'other': 0}
        for utterance in self.train:
            if utterance[len(utterance)-1][3] =="Punc":
                utterance = utterance[:len(utterance)-1]
            for i in range(len(utterance)):
                if utterance[i][3] in ["n:prop", "n:let", "n"]:
                    self.coverage['n'] += 1
                elif utterance[i][3] in ["v:mdl", "v:mdllex", "v:pos", "v"] :
                    self.coverage['v'] += 1
                else: 
                    self.coverage['other'] += 1
        print(self.coverage)
        self.coverage['total'] = self.coverage['n'] + self.coverage['v'] + self.coverage['other']
            
            
                      
def main(model, corpus, name_file_out, dossier_resultats, dossier_erreurs): 
    """
    Fonction qui prend en paramètre le chemin pour le corpus et le vocabulaire connu de l'enfant.
    Puis, on entraîne un modèle de contexte et on fait une validation croisée.
    Cette méthode écrit un rapport de l'évaluation dans le fichier "rapport_test.txt".
    @param model : le modèle à tester.
    @param corpus : le corpus de l'expérience.
    @param name_file_out : le nom du fichier qui sera crée.
    @param dossier_resultats : le dossier où les résultats devront être écrits.
    @param dossier_erreurs : le dossier où les analyses d'erreurs devront être écrites.
    """
    test_rapport = open(dossier_resultats+name_file_out, "w", encoding='utf-8')  # rapport du test du modèle
    test_rapport.write("k_fold\tprecision_n\tprecision_v\trappel_n\trappel_v\tnb_tri\tnb_bi\tnb_none\n")
    fa_n = open(dossier_erreurs+"fa_n_"+name_file_out, "w", encoding='utf-8')
    fa_v = open(dossier_erreurs+"fa_v_"+name_file_out, "w", encoding='utf-8')
    miss_n = open(dossier_erreurs+"miss_n"+name_file_out, "w", encoding='utf-8')
    miss_v = open(dossier_erreurs+"miss_v"+name_file_out, "w", encoding='utf-8')
    n=10  # validation croisée de six plis
    for i in range(0,n): 
        mini_corpus = []
        sous_corpus = Corpus("corrected_corpus/", 0.0005)
        for j in range(len(corpus)-i):
            if j% n== 0:
                mini_corpus.append(copy.deepcopy(corpus[j+i]))
        for k in range(len(mini_corpus)):
            if k%3==0:
                model.test.append(copy.deepcopy(mini_corpus[k]))
            else:
                model.train.append(copy.deepcopy(mini_corpus[k]))
        sous_corpus.utterances = copy.deepcopy(model.test)
        for utt in sous_corpus.utterances:
            sous_corpus.count_voca(utt)
        sous_corpus.get_freqlist()
        sous_corpus.get_test_vocab()
        model.test_vocab = copy.deepcopy(sous_corpus.test_vocab)
        print("k-fold", str(i),name_file_out)
        model.get_ngrams()
        model.do_the_test()
        
        if model.bien_pred_n+model.false_allarms_n != 0:
            pre_n = str(float(model.bien_pred_n)/(model.bien_pred_n+model.false_allarms_n))
        else :
            pre_n = str(0.0)
        if model.bien_pred_v+model.false_allarms_v != 0:
            pre_v = str(float(model.bien_pred_v)/(model.bien_pred_v+model.false_allarms_v))
        else:
            spre_v = str(0.0)
        if model.bien_pred_n+model.misses_n != 0:
            rap_n = str(float(model.bien_pred_n)/(model.bien_pred_n+model.misses_n))
        else:
            rap_n = str(0.0)
        if model.bien_pred_v+model.misses_v != 0.0:
            rap_v = str(float(model.bien_pred_v)/(model.bien_pred_v+model.misses_v))
        else :
            rap_v = str(0.0)
        nb_tri = str(model.relying_on_trigram)
        nb_bi = str(model.relying_on_bigram)
        nb_none =  str(model.cannot_find)
        test_rapport.write(str(i)+"\t"+pre_n+"\t"+pre_v+"\t"+rap_n+"\t"+rap_v+"\t"+nb_tri+"\t"+nb_bi+"\t"+nb_none+"\n")
        
        """
        Ecrire l'analyse des erreurs dans les fichiers appropriés.
        """
        model.get_neat_error_results(model.errors["fa_n"], model.false_allarms_n, fa_n, i )
        model.get_neat_error_results(model.errors["fa_v"], model.false_allarms_v, fa_v, i)
        model.get_neat_error_results(model.errors["miss_n"], model.misses_n, miss_n, i)
        model.get_neat_error_results(model.errors["miss_v"], model.misses_v, miss_v, i)
        
        """
        Reset du modèle pour le prochain pli de la validation crosiée.
        """
        model.test_vocab = []
        model.train = []
        model.test = []
        model.trigrams = {}
        model.bigrams = {}
        model.bien_pred_n = 0
        model.bien_pred_v = 0
        model.false_allarms_n = 0
        model.false_allarms_v = 0
        model.misses_n = 0
        model.misses_v = 0
        model.relying_on_bigram = 0
        model.relying_on_trigram =0
        model.cannot_find=0
        model.errors = {"fa_n": {}, "fa_v": {}, "miss_n":{}, "miss_v":{}}
        model.count_trigrammes = {}
    """
    Fermer les fichiers dans lesquels nous avons écrits.
    """   
    test_rapport.close()
    fa_n.close()
    fa_v.close()
    miss_n.close()
    miss_v.close()


def count_contexts(model, corpus, name_file_out): 
    """
    Fonction qui prend en paramètre le chemin pour le corpus et le vocabulaire connu de l'enfant.
    Puis, on entraîne un modèle de contexte et on fait une validation croisée.
    Cette méthode écrit un rapport de l'évaluation dans le fichier "rapport_test.txt".
    @param model : le modèle à tester.
    @param corpus : le corpus de l'expérience.
    @param name_file_out : le nom du fichier qui sera crée.
    """
    sous_corpus = Corpus("corrected_corpus/", 0.0005)
    for j in range(len(corpus)):
        if j%3== 0:
            model.test.append(copy.deepcopy(corpus[j]))
        else:
            model.train.append(copy.deepcopy(corpus[j]))
    sous_corpus.utterances = copy.deepcopy(model.test)
    for utt in sous_corpus.utterances:
        sous_corpus.count_voca(utt)
    sous_corpus.get_freqlist()
    sous_corpus.get_test_vocab()
    model.test_vocab = copy.deepcopy(sous_corpus.test_vocab)
    print(name_file_out)
    model.get_ngrams()
    model.do_the_test()
    
    """
    ici comptage des trigrammes utilisés par chaque modèle pour tous les plis de la validation croisée
    """

    trigr = open("count_trigrammes/"+name_file_out, "w", encoding='utf-8')
    trigr.write("contexte\tnb_utilisations\tnb_cilbe_n\tnb_cible_v\tréponse_mod\n")
    for tr in model.count_trigrammes:
        trigr.write(tr + "\t"
                    +str(model.count_trigrammes[tr]['ut'])+"\t"
                    +str(model.count_trigrammes[tr]['n'])+"\t"
                    +str(model.count_trigrammes[tr]['v'])+"\t"
                    + str(model.count_trigrammes[tr]['rep'])+"\n")
            
    trigr.close()



"""
Produire les différentes graines sémantiques
"""
corp = Corpus("corrected_corpus/", 0.0005)
corp.get_voca_and_utterances()
corp.get_freqlist()
vocab0 = corp.get_graine_semantique(8,1)
print ("V0")
str_v0 = ""
for w in vocab0:
    w = w.strip()
    str_v0 = str_v0 + w + ", "
print (str_v0 + "\n")


vocab1 = corp.get_graine_semantique(16,2)
print ("V1")
str_v1 = ""
for w in vocab1:
    w = w.strip()
    str_v1 = str_v1 + w + ", "
print (str_v1 + "\n")


vocab2 = corp.get_graine_semantique(32,3)
print ("V2")
str_v2 = ""
for w in vocab2:
    w = w.strip()
    str_v2 = str_v2 + w + ", "
print (str_v2 + "\n")


vocab3 = corp.get_graine_semantique(64,6)
print ("V3")
str_v3 = ""
for w in vocab3:
    w = w.strip()
    str_v3 = str_v3 + w + ", "
print (str_v3 + "\n")


vocab4 = corp.get_graine_semantique(128,12)
print ("V4")
str_v4 = ""
for w in vocab4:
    w = w.strip()
    str_v4 = str_v4 + w + ", "
print (str_v4 + "\n")


vocab5 = corp.get_graine_semantique(192,24)
print ("V5")
str_v5 = ""
for w in vocab5:
    w = w.strip()
    str_v5 = str_v5 + w + ", "
print (str_v5 + "\n")

print("Pour continuer, appuyez maintenant sur une touche")
input()

"""
Prendre le corpus sous forme de liste d'énoncés.
Prendre la liste de vocabulaire de test.
""" 
utt = open("utterances", 'rb')
corpus = pickle.load(utt)
utt.close()


"""
Arguments du programme: 
- le chemin vers le dossier dans lequel les résultats seront stockés.
- le chemin vers le dossier dans lequel les analyses d'erreurs seront stockées.
"""
parser = argparse.ArgumentParser()
parser.add_argument("dossier_resultats", help="Dossier pour les fichiers avec les résultats des différents modèles. 'resultats\\\\' pour windows (premier \\ pour échaper le symbôle regex \\) et 'resultats/' pour linux")
parser.add_argument("dossier_erreurs", help="Dossier pour les fichiers output des analyses d'erreurs. 'erreurs\\\\' pour windows (premier \\ pour échaper le symbôle regex \\) et 'erreurs/' pour linux")
args  = parser.parse_args()
dossier_resultats = args.dossier_resultats
dossier_erreurs = args.dossier_erreurs


"""
Effectuer les test pour tous les modèles et toutes les graines sémantiques. 
"""
model_vm_baseline = Modele_Baseline_Vm([], [], [], [])
main(model_vm_baseline, corpus, "modele_baseline_vm.txt",dossier_resultats, dossier_erreurs)

model_v0_baseline = Modele_Baseline(vocab0, [], [], [])
main(model_v0_baseline, corpus, "modele_baseline_v0.txt",dossier_resultats, dossier_erreurs)

model_v1_baseline = Modele_Baseline(vocab1, [], [], [])
main(model_v1_baseline, corpus, "modele_baseline_v1.txt",dossier_resultats, dossier_erreurs)

model_v2_baseline = Modele_Baseline(vocab2, [], [], [])
main(model_v2_baseline, corpus, "modele_baseline_v2.txt",dossier_resultats, dossier_erreurs)

model_v3_baseline = Modele_Baseline(vocab3, [], [], [])
main(model_v3_baseline, corpus, "modele_baseline_v3.txt",dossier_resultats, dossier_erreurs)

model_v4_baseline = Modele_Baseline(vocab4, [], [], [])
main(model_v4_baseline, corpus, "modele_baseline_v4.txt",dossier_resultats, dossier_erreurs)

model_v5_baseline = Modele_Baseline(vocab5, [], [], [])
main(model_v5_baseline, corpus, "modele_baseline_v5.txt",dossier_resultats, dossier_erreurs)

model_v0_imbrique = ModeleContextesImbriques(vocab0, [], [], [])
main(model_v0_imbrique, corpus, "modele_imbrique_v0.txt",dossier_resultats, dossier_erreurs)

model_v1_imbrique = ModeleContextesImbriques(vocab1, [], [], [])
main(model_v1_imbrique, corpus, "modele_imbrique_v1.txt",dossier_resultats,dossier_erreurs)

model_v2_imbrique = ModeleContextesImbriques(vocab2, [], [], [])
main(model_v2_imbrique, corpus, "modele_imbrique_v2.txt",dossier_resultats,dossier_erreurs)

model_v3_imbrique = ModeleContextesImbriques(vocab3, [], [], [])
main(model_v3_imbrique, corpus, "modele_imbrique_v3.txt",dossier_resultats,dossier_erreurs)

model_v4_imbrique = ModeleContextesImbriques(vocab4, [], [], [])
main(model_v4_imbrique, corpus,"modele_imbrique_v4.txt",dossier_resultats,dossier_erreurs)

model_v5_imbrique = ModeleContextesImbriques(vocab5, [], [], [])
main(model_v5_imbrique, corpus, "modele_imbrique_v5.txt",dossier_resultats,dossier_erreurs)

model_vm_imbrique = Modele_Imbrique_Vm([], [], [], [])
main(model_vm_imbrique, corpus, "modele_imbrique_vm.txt",dossier_resultats,dossier_erreurs)

model_v0_gauche = ModeleContextesGauches(vocab0, [], [], [])
main(model_v0_gauche, corpus, "modele_gauche_v0.txt",dossier_resultats,dossier_erreurs)

model_v1_gauche = ModeleContextesGauches(vocab1, [], [], [])
main(model_v1_gauche, corpus, "modele_gauche_v1.txt",dossier_resultats,dossier_erreurs)

model_v2_gauche = ModeleContextesGauches(vocab2, [], [], [])
main(model_v2_gauche, corpus, "modele_gauche_v2.txt",dossier_resultats,dossier_erreurs)

model_v3_gauche = ModeleContextesGauches(vocab3, [], [], [])
main(model_v3_gauche, corpus, "modele_gauche_v3.txt",dossier_resultats,dossier_erreurs)

model_v4_gauche = ModeleContextesGauches(vocab4, [], [], [])
main(model_v4_gauche, corpus, "modele_gauche_v4.txt",dossier_resultats,dossier_erreurs)

model_v5_gauche = ModeleContextesGauches(vocab5, [], [], [])
main(model_v5_gauche, corpus, "modele_gauche_v5.txt",dossier_resultats,dossier_erreurs)

model_vm_gauche = Modele_Gauche_Vm([], [], [], [])
main(model_vm_gauche, corpus, "modele_gauche_vm.txt",dossier_resultats,dossier_erreurs)

model_v0_droit = ModeleContextesDroits(vocab0, [], [], [])
main(model_v0_droit, corpus, "modele_droit_v0.txt",dossier_resultats,dossier_erreurs)

model_v1_droit = ModeleContextesDroits(vocab1, [], [], [])
main(model_v1_droit, corpus, "modele_droit_v1.txt",dossier_resultats,dossier_erreurs)

model_v2_droit = ModeleContextesDroits(vocab2, [], [], [])
main(model_v2_droit, corpus, "modele_droit_v2.txt",dossier_resultats,dossier_erreurs)

model_v3_droit = ModeleContextesDroits(vocab3, [], [], [])
main(model_v3_droit, corpus, "modele_droit_v3.txt",dossier_resultats,dossier_erreurs)

model_v4_droit = ModeleContextesDroits(vocab4, [], [], [])
main(model_v4_droit, corpus, "modele_droit_v4.txt",dossier_resultats,dossier_erreurs)

model_v5_droit = ModeleContextesDroits(vocab5, [], [], [])
main(model_v5_droit, corpus, "modele_droit_v5.txt",dossier_resultats,dossier_erreurs)

model_vm_droit = Modele_Droit_Vm([], [], [], [])
main(model_vm_droit, corpus, "modele_droit_vm.txt",dossier_resultats,dossier_erreurs)

count_contexts(model_vm_imbrique, corpus,"trigrams_vm_imbrique.txt")
count_contexts(model_vm_gauche, corpus,"trigrams_vm_gauche.txt")
count_contexts(model_vm_droit, corpus,"trigrams_vm_droit.txt")
