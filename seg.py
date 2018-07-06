# coding: utf-8
#!/usr/bin/env python
import pyarabic.araby as araby
import pyarabic.number as number
import stopwords_classified
import tashaphyne
import tashaphyne.stemming 

def split_accourding_quotion(wordlist):
	try:
		wordlist=[x.decode('utf8') for x in wordlist]
	except Exception as e:
		pass
	sen=[]
	db="no"
	for x in wordlist:
		if x==u'"' :
			if db=="no":
				s=[]
				db="yes"
			elif db=="yes":
				db="no"
				sen.append('"'+" ".join(s)+'"')
				s=[]
		elif db=="yes" :
			s.append(x)
		elif db=="no":
			sen.append(x)
	return sen

def split_accourding_numbers(wordlist):

	try:
		try:
			wordlist=[x.decode('utf8') for x in wordlist]
		except Exception as e:
			pass
		lst=number.detect_numbers(wordlist)
		sen=[]
		s=""
		for i in xrange(len(lst)):
			if lst[i]==u'DB':
				s=""
				s+=wordlist[i]
			elif lst[i]==u'DI':
				s+=" "+wordlist[i]
			else :
				if s!="":
					sen.append(s)
					s=""
					sen.append(wordlist[i])
		if s!="":
			sen.append(s)
		return sen
	except Exception as e:
		return wordlist
"""
def split_accourding_numbers(wordlist):
	#read list of named entities
	path_named_entity="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/benajiba/named_entity"
    lst_named_entities=open(path_named_entity,'r').read().split()
    lst_named_entities=[item.decode('utf8') for item in lst_named_entities]
    lst_named_entities=[unicodedata.normalize('NFKD',item) for item in lst_named_entities]
    lst_named_entities=[clean_str(item) for item in lst_named_entities]

    item=""
    for x in xrange(len(wordlist)):
    	if wordlist[x] in lst_named_entities:
    		if etat='begin':
    			item='"'+wordlist[x]
    		else
"""


def stem(word):
	try:
		wordlist=[x.decode('utf8') for x in wordlist]
	except Exception as e:
		pass
	CUSTOM_PREFIX_LIST = [u'كال', u'أفبال', u'أفك', u'فك', u'أولل', u'', u'أف', u'ول', u'أوال', u'ف', u'و', u'أو', u'ولل', u'فب', u'أول', u'ألل', u'لل', u'ب', u'وكال', u'أوب', u'بال', u'أكال', u'ال', u'أب', u'وب', u'أوبال', u'أ', u'وبال', u'أك', u'فكال', u'أوك', u'فلل', u'وك', u'ك', u'أل', u'فال', u'وال', u'أوكال', u'أفلل', u'أفل', u'فل', u'أال', u'أفكال', u'ل', u'أبال', u'أفال', u'أفب', u'فبال']
	CUSTOM_SUFFIX_LIST = [u'كما', u'ك', u'هن', u'ي', u'ها', u'', u'ه', u'كم', u'كن', u'هم', u'هما', u'نا']

	# create a cعstomized stemmer object for stemming enclitics and procletics
	custom_stemmer = tashaphyne.stemming.ArabicLightStemmer()

	# configure the stemmer object
	custom_stemmer.set_prefix_list(CUSTOM_PREFIX_LIST)
	custom_stemmer.set_suffix_list(CUSTOM_SUFFIX_LIST)
	custom_stemmer.segment(word)
	lst=custom_stemmer.get_affix_list()
 	lst=[x['root'] for x in lst]
 	lst_len=[len(x) for x in lst]
 	lst=[x for x in lst if len(x)==min(lst_len)]
 	return lst[0]

def set_list(wordlist):
	lst=[]
	for x in wordlist:
		if x not in lst:
			lst.append(x)
	return lst

def quotation_named_entities(wordlist):
	try:
		try:
			wordlist=[x.decode('utf8') for x in wordlist]
		except Exception as e:
			pass
		lst=number.detect_numbers(wordlist)
		sen=[]
		s=""
		for i in xrange(len(lst)):
			if lst[i]==u'DB':
				s=""
				s+=wordlist[i]
			elif lst[i]==u'DI':
				s+=" "+wordlist[i]
			else :
				if s!="":
					sen.append(s)
					s=""
					sen.append(wordlist[i])
		if s!="":
			sen.append(s)
		return sen
	except Exception as e:
		return wordlist

def quotation_between_named_entities(lst):
	debut="no"
	fin="no"
	named_entity=[]
	new_lst=[]
	for x in lst:
		if x in named_entities:
			if debut=="no":
				debut="yes"
				named_entity.append('"')
				named_entity.append(x)
			elif debut=="yes":
				named_entity.append(x)
		else:
			if len(named_entity)>1:
				named_entity.append('"')
				new_lst.append(" ".join(named_entity))
			named_entity=[]
			debut="no"
			new_lst.append(x)
	return new_lst



#print dir(number)
"""
print split_accourding_numbers(u"السلام")


tutorial
lst=split_accourding_numbers(wordlist,'yes')
lst1=split_accourding_quotion(wordlist1,'yes')
stem(word)
"""

