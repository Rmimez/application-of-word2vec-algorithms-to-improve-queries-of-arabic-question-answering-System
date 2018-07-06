##******************************************************************************************
##Application of Word2Vec Algorithms to Improve Queries of Arabic Question Answering System.
##university     : University of Yahia Fares -Medea-
##project        : Submitted for graduation project in computer science master
##Specialty      : Systems Engineering and Web Technology
##Version        : 0.1
##Author         : HACHEMI Mohamed Ramzi
##Directed By    : Mazari Ahmed Chrif
##Source         : https://github.com/Rmimez/Word2vec-for-arabic-
#Accademic year  : 2017/2018
##*****************************************************************************************

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

path_nn="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/result final7/google_results0/queries_answers.csv"
path_sg="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/result final7/google_results1/queries_SG_answers.csv"
path_cbow="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/result final7/google_results1/queries_CBOW_answers.csv"
path_sg4="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/result final7/google_results4/queries_SG_answers.csv"
path_cbow4="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/result final7/google_results4/queries_CBOW_answers.csv"
path_sg_2="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/older method/google_results6/other results/queries_SG_answers.csv"
path_cbow_2="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/older method/google_results6/other results/queries_CBOW_answers1.csv"
path_sg_3="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/wor2vec finale/search_results/google_results6/other results/queries_CBOW_answers1.csv"

def read_csv(path,column="pertinent",fon="data"):
	with open(path) as csvfile:
		reader = csv.DictReader(csvfile)
		lst=[]
		for row in reader:
			lst.append(row[column])
	lst= [lst[x:x+10] for x in xrange(0, len(lst), 10)]
	if fon!="data":
		return lst[:50]
	lst1=[]
	for x in lst:
		lst1.append(x.count('yes'))
	lst1=lst1[:50] #juste 50 reponces sou form list
	return lst1

def data(path_nn,path_model):
	lst=read_csv(path_nn)
	lst1=read_csv(path_model)
	index=1
	arr = np.empty((0,3), int)
	for i in xrange(len(lst)):
		arr = np.append(arr, np.array([[index,lst[i],lst1[i]]]), axis=0)
		index+=1
	print arr
	return arr

def count_positive(lst):
	i=0
	d=0
	n=0
	for x in lst:
		if float(x)>0:
			i+=1
		elif float(x)<0:
			d+=1
		else:
			n+=1
	return i,d,n

def set_list(wordlist):
	lst=[]
	for x in wordlist:
		if x not in lst:
			lst.append(x)
	return lst

def function1(path_nn,path_sg,path_cbow):
	lst_nn=read_csv(path_nn)
	lst_sg=read_csv(path_sg)
	lst_cbow=read_csv(path_cbow)
	lst_sg_cbow=read_csv(path_sg,"Query",fon="fun")
	lst_c_sg_cbow=[[a.count(')') for a in x] for x in lst_sg_cbow]
	lst_c_sg_cbow=[x[0] for x in lst_c_sg_cbow]
	l1=[lst_c_sg_cbow.count(x) for x in set(lst_c_sg_cbow)]

	print lst_nn
	print lst_sg
	print lst_cbow
	lst_marge_sg=[lst_sg[x]-lst_nn[x] for x in xrange(len(lst_nn))]
	lst_marge_cbow=[lst_cbow[x]-lst_nn[x] for x in xrange(len(lst_nn))]
	sum_sg=[]
	sum_cbow=[]
	
	
	lst=lst_marge_sg
	print '*******************************************'
	i,d,n= count_positive(lst)
	print i
	print d
	print n
	print '*******************************************'


	lst=lst_marge_cbow
	print lst
	print '*******************************************'
	i,d,n= count_positive(lst)
	print i
	print d
	print n
	print'*******************************' 

function1(path_nn,path_sg,path_cbow)