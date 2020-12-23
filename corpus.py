#!/usr/bin/env python # -*- coding: utf-8 -*-
import os, copy, io


class Corpus():
    """
    Cette classe permet de parcourir les fichiers connl du corpus.
    Elle découpe le corpus en énoncées et permet de faire des statistiques sur les types et les tokens
    pour les différentes catégories syntaxiques.
    Elle permet de trouver les mots qui ont une fréquence de moins de 0.0005 (les mots pour lesquels une prédiction
    sera faite par les modèles).
    """
    
    
    def __init__(self, rootdir, seuil):
        self.seuil = seuil  # seuil de fréquence pour qu'on mot soit pris comme objet de prédiction
        self.rootdir = rootdir  # le dossier dans lequel se trouvent les fichiers connl du corpus
        self.utterances = []  # ensemble d'énoncées du corpus
        self.voca = {}  # structure pour stocker le vocabulaire du corpus
        self.freq_list = []  # une liste dans laquelle les mots avec leurs fréquences sont stockés
        self.noms_et_verbes = {"n":{}, "v":{}}  # une structure où l'on compte les lemmes des noms et des verbes par fréquence
        self.test_vocab = []  # ensemble de mots avec une fréquence inférieure à 0.0005 
        
        #Retour au double flux normal sans unité gs
        self.action_verbs = []
        self.noms_concrets = []
        ac_vrb = open("verbes_actions.txt", 'r', encoding='utf-8')
        line = ac_vrb.readline()
        while line:
            self.action_verbs.append(line.split("\n")[0].strip())
            line = ac_vrb.readline()
        ac_vrb.close()
        n_concret = open("noms_concrets.txt", 'r',  encoding='utf-8')
        line = n_concret.readline()
        while line:
            self.noms_concrets.append(line.split("\n")[0].strip())
            line = n_concret.readline()
        n_concret.close()
        
        
    def get_voca_and_utterances(self):
        """
        Méthode qui sert à parcourir le corpus pour trouver son vocabulaire.
        """
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                f = open(self.rootdir+file,'r', encoding='utf-8')
                self.get_voca_aux(f)
                f.close()
        

    def get_voca_aux(self, fichier):
        """
        Méthode auxilliaire de la méthode "get_voca". 
        Cette méthode parcourt un fichier et trouve toutes ses énoncées. Puis, il compte les formes de mots dans chaque énoncée ansi que 
        la classe morpho-syntaxique à laquelle ce mot appartient dans ce contexte. 
        La fonction compte également le nombre d'occurrences des lemmes des Noms et des Verbes dans le corpus.
        @param fichier: le fichier que la fonction doit parcourir.
        """
        print(fichier)
        line = fichier.readline()
        while line != "":
            utterance = []
            while line != '\n' and line !="\r\n":
                utterance.append(line.split())
                line = fichier.readline()
            line = fichier.readline()
            utterance = self.normaliser_apostrophes(utterance)
            utterance = self.cut_out_cm(utterance)
            self.utterances.append(utterance)
            self.count_voca(utterance)


    def count_voca(self, utterance):
            """
            Ajoute les comptages d'un énoncé au comptage total.
            @param utterance: un énoncé pour laquelle un comptage sera fait.
            """
            for tok in utterance:
                cat = copy.deepcopy(tok[3])
                if cat!= "Punc":     
                    if tok[1] not in self.voca:
                        self.voca[tok[1]] = {cat:1}
                    else:
                        if cat not in self.voca[tok[1]]:
                            self.voca[tok[1]][cat] = 1
                        else:
                            self.voca[tok[1]][cat] = self.voca[tok[1]][cat] + 1
                if cat in ["n", "n:let"]:
                    if tok[2] in self.noms_et_verbes["n"]:
                        self.noms_et_verbes["n"][tok[2]] = self.noms_et_verbes["n"][tok[2]] +1
                    else:
                        self.noms_et_verbes["n"][tok[2]] = 1
                if cat in ["v:mdl", "v:mdllex", "v:pos", "v"]:
                    if tok[2] in self.noms_et_verbes["v"]:
                        self.noms_et_verbes["v"][tok[2]] = self.noms_et_verbes["v"][tok[2]]+1
                    else:
                        self.noms_et_verbes["v"][tok[2]] = 1
                   
                        
    def get_graine_semantique(self, nb_n, nb_v):
        """
        Retourne la graine sémantique en se basant sur self.utterances.
        @param nb_n : nombre de noms que la graine sémantique doit contenir
        @param nb_v : nombre de verbes que la graine sémantique doit contenir
        """
        """"
        freqs_n = []
        freqs_v = []
        for n in self.noms_et_verbes['n']:
            freqs_n.append((n, self.noms_et_verbes['n'][n]))
        for v in self.noms_et_verbes['v']:
            freqs_v.append((v, self.noms_et_verbes['v'][v]))
        freqs_n = sorted(freqs_n, reverse=True,key=lambda x: x[1])
        freqs_v = sorted(freqs_v, reverse=True,key=lambda x: x[1])
        freqs_n = list(map((lambda x: x[0]), freqs_n))
        freqs_v = list(map((lambda x: x[0]), freqs_v))
        graine_s = freqs_n[:nb_n]
        graine_s.extend(freqs_v[:nb_v])
        return graine_s
        """
        
        graine_n = []
        graine_v = []
        n_actuel = 0
        v_actuel = 0
        i = 0
        while i < nb_n:
            graine_n.append(self.noms_concrets[i])
            i = i + 1
        j = 0
        while j < nb_v:
            graine_v.append(self.action_verbs[j])
            j = j + 1
        graine_s = copy.deepcopy(graine_n)
        graine_s.extend(copy.deepcopy(graine_v))
        print ("pourcentage n", self.get_percentage('n', graine_n))
        print ("pourcentage v", self.get_percentage('v', graine_v))
        print ("nb n",i)
        print ("nb v", j)
        return graine_s
        
#         print "ok"
#         graine_n = []
#         graine_v = []
#         i = 0
#         while i < nb_n:
#             graine_n.append(self.noms_concrets[i].strip())
#             i = i + 1
#         j = 0
#         while j < nb_v:
#             graine_v.append(self.action_verbs[j].strip())
#             j = j + 1
#         graine_s = copy.deepcopy(graine_n)
#         graine_s.extend(copy.deepcopy(graine_v))
#         print "nb n",i
#         print "nb v", j
#         print "percentage n, ", self.get_percentage('n', graine_n)
#         print "percentage v, ", self.get_percentage('v', graine_n)
#         return graine_s

    
    def get_percentage(self, n_ou_v, word_list):
        """
        Trouve le pourcentage de tokens couvert par la graine sémantique.
        @param n_ou_v : s'il s'agit des Noms ou des Verbes
        @param word_list : la liste de mots des noms et des verbes qui va aller dans la graine sémantique
        """
        occ =0
        counts = self.get_nb_toks_nb_pos()[1]
        tot= counts[n_ou_v]
        for x in word_list:
            occ = occ + self.noms_et_verbes[n_ou_v][x]
        return float(occ)/float(tot)*100
  
  
    def get_nb_toks_nb_pos(self):
        """
        Calcule le nombre de tokens du corpus, ansi que le nombre d'occurrences pour chaque catégorie morpho-syntaxique.
        convert_pos sert à regrouper les tags morphosyntaxiques d'une façon plus dense.
        """
        convert_pos = {'pro': ['pro', 'pro:y', 'pro:int', 'pro:rel', 'pro:refl', 'pro:obj', 'pro:sub', 'pro:subj', 'pro:dem'], 
                       'v':['v:pos', 'v:mdl', 'v', 'v:mdllex', 'v:poss'], 'n':['n:let', 'n'], 'co':['co'], 
                       'adv':['adv:adj', 'adv', 'adv:neg', 'adv:place', 'adv:int'], 'meta':['meta'],
                       'prep':['prep'], '?':['?'], 'adj':['adj'], 'conj':['conj'], 'n:prop': ['n:prop'], 
                       'det':['det:dem', 'det', 'det:poss', 'det:gen'], 'num':['int', 'num'], 'on':['on'],
                       'cm':['cm'], 'qn':['qn']}
        nb_tok = 0
        pos_count = {}
        for forme in self.voca:
            for pos in self.voca[forme]:
                new_pos = pos
                for tag in convert_pos:
                    if pos in convert_pos[tag] :
                        new_pos = tag
                nb_tok = nb_tok + self.voca[forme][pos]
                if new_pos in pos_count:
                    pos_count[new_pos] = pos_count[new_pos] + self.voca[forme][pos]
                else:
                    pos_count[new_pos] = self.voca[forme][pos]
        return (nb_tok, pos_count) 
            
            
    def get_info_voca(self):
        """
        Imprime à l'écran quelques informations essentielles sur le vocabulaire du corpus:
        - le nombre de types
        - le nombre de tokens
        - le nombre de types de noms (comptés par lexèmes)
        - le nombre de types de verbes (comptés par lexèmes)
        - le nombre d'occurence pour chaque catégorie morpho-syntaxique
        """
        (nb_tok, pos_count) = self.get_nb_toks_nb_pos()
        nb_types = len(self.voca.keys())
        print ("le nombre de tokens du corpus:", nb_tok)
        print ("le nombre de types du corpus:", nb_types)
        print ("le nombre de types de noms:", str(len(self.noms_et_verbes["n"])))
        print ("le nombre de types de verbe:", str(len(self.noms_et_verbes["v"])))
        print ("voici le nombre de tokens pour chaque catégorie:")
        for pos in pos_count:
            print (pos + "\t"+ str(pos_count[pos]))


    def get_info_utterances(self):
        """
        Imprime à l'écran le nombre d'énoncés du corpus.       
        """
        print ("le nombre d'énoncés du corpus:", str(len(self.utterances)))
        
            
    def write_voca_into_file(self):
        """
        Cette méthode écrit le comptage des tokens dans un fichier.
        """
        file = open("frequence_voca.txt", 'w', encoding='utf-8')
        for (forme, freq) in self.freq_list:
            to_write = forme + "\t" + str(freq) + "\n"
            file.write(to_write)
        file.close()
        
        
    def get_freqlist(self):
        """
        Constiue une liste des formes triées par leur fréquence (freqlist).
        Calcule le total des tokens du corpus.
        """
        for forme in self.voca: 
            freq = 0
            for pos in self.voca[forme]:
                freq=freq + self.voca[forme][pos]
            self.freq_list.append((forme, freq))
        self.freq_list = sorted(self.freq_list, reverse=True,key=lambda x: x[1])
        self.total_tokens = sum([pair[1] for pair in self.freq_list])
        
        
    def get_test_vocab(self):
        """
        Méthode qui utlise un seuil de fréquence self.seuil pour déterminer quels mots doivent constituer le vocabulaire cible.
        (Ensemble de mots pour lesquels on fait une prédiction de catégorie morpho-syntaxique).
        """
        for i in range(len(self.freq_list)):
            if float(self.freq_list[i][1])/float(self.total_tokens) < self.seuil:
                test_vocab = self.freq_list[i:]
                self.test_vocab = [pair[0] for pair in test_vocab]
                break


    def normaliser_apostrophes(self, utterance):
        """
        Dans les fichiers connl du corpus, quand il y a deux tokens reliés avec une apostrophe, 
        cette méthode permet de les affichier correctement dans les énoncées du programme.
        """
        for j in range(len(utterance)):
            if utterance[j][1][0] =="$":
                utterance[j][1] = utterance[j][1][2:]
                bfr1 = ""
                bfr2 = ""
                i = 0
                while utterance[j][1][i] != "'":
                    bfr1 = bfr1 + utterance[j][1][i]
                    i = i + 1
                bfr1 = bfr1 + "'"
                bfr2 = utterance[j][1][i+1:]
                utterance[j][1] = bfr1
                utterance[j + 1][1] = bfr2 
        return utterance
    
    
    def cut_out_cm(self, utterance):
            """
            Permet de supprimer les virgules qui fonctionnent comme marqueurs prosodiques dans le corpus.
            """
            i = 0
            while i < len(utterance):
                if utterance[i][3]=="cm":
                    new_utterance = copy.deepcopy(utterance[:i])
                    if i != len(utterance)-2:
                        new_utterance.extend(copy.deepcopy(utterance[i+1:]))
                    utterance = self.cut_out_cm(new_utterance)
                i = i + 1
            return utterance
        
        