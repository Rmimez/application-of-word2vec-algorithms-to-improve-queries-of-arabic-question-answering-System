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

# coding: utf-8
#!/usr/bin/env python
from google import google
import csv
import time 

class Google_answers():
	"""in this class we see functions for getting google results of queries
		and u should define 2 parameter:
		path_queries : that mean the path of reformulated queries
		saved_path : it's for saving file as csv format contain google answers
	"""
	def __init__(self):
		super(Google_answers, self).__init__()

	def read_data(path):
		f=open(path,"r")
		lst=f.readlines()
		lst=[item.split() for item in lst]
		lst=[' '.join(str(x) for x in item[4:]) for item in lst]
		return lst

	def google_answers_and_export(path_queries,saved_path):
		lst=read_data(path_queries)
		f=open('/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/benajiba/ArabicAnswerss',"r")
		answers=f.readlines()
		csvfile= open(saved_path, 'w')
		fieldnames = ['Query','Answer', 'Link','Title','Description','pertinent']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		index=0
		for x in lst:
			time.sleep(1)
			print x
			search_results = google.search(x.decode('utf8'),2)
			i=0
			for item in search_results:
				if (i<10):
					link=item.link
					name=item.name
					description=item.description
					pertinent=u"no"
					ans=answers[index]
					writer.writerow({'Query': x,'Answer':ans,'Link': link,'Title': name.encode('utf8'), 'Description': description.encode('utf8'),'pertinent':'no'})
					i+=1
			index+=1
		csvfile.close()

if __name__ == '__main__':

	#example
	path_queries="test01/CBOW_quiries.txt"
	saved_path="test01/queries_CBOW_answers.csv"

	google_answers=Google_answers()
	google_answers.google_answers_and_export(path_queries,saved_path)


"""
GoogleResult:
    self.name # The title of the link
    self.link # The external link
    self.google_link # The google link
    self.description # The description of the link
    self.thumb # The link to a thumbnail of the website (NOT implemented yet)
    self.cached # A link to the cached version of the page
    self.page # What page this result was on (When searching more than one page)
    self.index # What index on this page it was on"""