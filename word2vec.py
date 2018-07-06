##******************************************************************************************
##Application of Word2Vec Algorithms to Improve Queries of Arabic Question Answering System.
##university     : University of Yahia Fares -Medea-
##project        : Submitted for graduation project in computer science master
##Specialty      : Systems Engineering and Web Technology
##Version        : 0.1
##Author         : HACHEMI Mohamed Ramzi
##Directed By    : Mazari Ahmed Chrif
##Source         : https://github.com/Rmimez/application-of-word2vec-algorithms-to-improve-queries-of-arabic-question-answering-System/edit/master/word2vec.py
#Accademic year  : 2017/2018
##*****************************************************************************************
# coding: utf-8
#!/usr/bin/env python

"""
yes    Option1--> normalizing                                 
yes    Option2--> remove stop words| fixed
yes    Option3--> stemming item of queries 
yes    Option4--> str2int 
yes    Option5--> int2str
yes    Option6--> fixé les entités nommées 
yes    Option7--> les ""
yes    Option8--> similarwords to others using word2vec 
yes    Option9--> using doesn't match for remove words that have meaning very far about general        meaning of sentence using word2vec
yes    Option10--> steaming exports similar words using tashaphine  
not    Option11--> use metrics for tell us about comparaison --> %
not    Option12--> timer
***************************make entiti nommée dabord************************
seuil
Experiences:
    1)Option1+option2(fixed)+option5+Option6+option8
    2)Option1+Option2(Remove)+Option6+Option7+Option8
    3)Option1+Option2(Remove)+Option6+Option7+Option8+Option10
    4)Option1+Option2(Remove)+Option6+Option7+option8+option9+Option10
    5)Option1+Option2(Remove)+Option6+Option7+option8+Option10+seuil
apprentissage des model parapport les text *********************
mtrics for compariason https://gist.github.com/bwhite/3726239
"""
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from gensim import corpora,models,similarities
from google import google
import re
import string
import unicodedata
import pyarabic.araby as araby
import pyarabic.number as number
import stopwords_classified
import seg
import unicodedata as ud

def punctuation_ar(txt): # this function for token all of the text with deleting punctuation ''.join(c for c in s if not ud.category(c).startswith('P'))
    txt1=""
    for c in txt:
        if c=='"':
            txt1+=c
        elif ud.category(c).startswith('P'):
            pass
        else:
            txt1+=c
    return ''.join(c for c in txt if c not in [u'.',u',',u'،',u'؟'])
    
def quotation_between_named_entities(lst,named_entities):
    lst.append(" ")
    named_entity=[]
    new_lst=[]
    for x in xrange(len(lst)):
        try:
            lst[x]=unicodedata.normalize('NFKD',lst[x])
        except Exception as e:
            pass
        finally:
            if lst[x] in named_entities:
                named_entity.append(lst[x])
            else:
                if len(named_entity)>1:
                    word='"'+" ".join(named_entity)+'"'
                    new_lst.append(word)
                elif len(named_entity)==1:
                    new_lst.append(named_entity[0])
                new_lst.append(lst[x])
                named_entity=[]
    return new_lst[::1]

def set_list(wordlist):
    lst=[]
    for x in wordlist:
        if x not in lst:
            lst.append(x)
    return lst

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def str2int(number):
	lst_n_roman=[('I','1',u'الاول'),('II','2',u'الثاني'),('III','3',u'الثالث'),('IV','4',u'الرابع'),('V','5',u'الخامس'),('VI','6',u'السادس'),('VII','7',u'السابع'),('VIII','8',u'الثامن'),('IX','9',u'التاسع'),('X','10',u'العاشر')]
	for x,y,z in lst_n_roman:
		if number==z:
			return '( '+x+' | '+z+')'
	return False

def read_Q_data(path):
    f=open(path,"r")
    lst=f.readlines()
    lst=[item.split() for item in lst]
    lst=[item[4:] for item in lst]
    return lst

def clean_str(text): #Option1--> normalizing
    search = [u"أ",u"إ",u"آ",u"ة",u"_",u"-",u"/",u".",u"،",u" و ",u" يا ",u'"',u"ـ",u"'",u"ى",u"\\",u'\n', u'\t',u'&quot;',u'?',u'؟',u'!']
    replace = [u"ا",u"ا",u"ا",u"ه",u" ",u" ",u"",u"",u"",u" و",u" يا",u' " ',u"",u"",u"ي",u"",u' ', u' ',u' ',u' ',u' ',u' ! ']
    text=araby.normalize_ligature(text)
    text=unicodedata.normalize('NFKD',text)
    text=araby.strip_tashkeel(text)#remove tashkeel
    p_longation = re.compile(r'(.)\1+')#remove longation
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)
    text = text.replace(u'وو', u'و')
    text = text.replace(u'يي', u'ي')
    text = text.replace(u'اا', u'ا')
    for i in range(0, len(search)):
        text = text.replace(unicodedata.normalize('NFKD',search[i]), unicodedata.normalize('NFKD',replace[i]))
    #trim
    text = text.replace(u'ئ', u'ئ')
    text = text.strip()
    return text

#numerical system
def text2numbers(item):
    return text2number(item)
# the first is named entities


def similar_word(model,sentence,word,named_entities,central_words):
# find and print the most similar terms to a word
    val_sim_central_words=0.7
    val_sim=0.7
    if RepresentsInt(word) :
        an= number.ArNumbers()
    elif stopwords_classified.this_is_stop_word(word):
        return '' #Remove Stop words
    elif word in named_entities:
        return word #Option6--> fixé les entités nommées 
    elif word in central_words:
        val_sim=val_sim_central_words;
    try:
        word_compose=word
        origin_word=word
        print origin_word
        word_compose=word_compose.split()
        if len(word_compose)>1:
            return word
        word=clean_str(word)
        most_similar = model.wv.most_similar( araby.normalize_ligature(word))
        lst=[x for x,y in most_similar if y>val_sim]
        lst=[''.join(c for c in x if c not in string.punctuation) for x in lst]
        if len(lst)==0:
            return origin_word
        lst=[seg.stem(x) for x in lst] #option10
        lst.insert(0,word) #insertion de mots source est obligatoire
        lst=set_list(lst)
        if len(lst)==1:
            return origin_word
        return '(' +(u' | '.join(lst))+')' #Option8--> similarwords to others using word2vec 
    except Exception as e:
        return origin_word

#function to build and refomulize queries
def queries(model,lst,named_entities,central_words):
    rank=0
    query_global=[]
    for x in lst:
        query_final=[]
        x=' '.join(x)
        x=punctuation_ar(x.decode('utf8'))
        x=seg.split_accourding_quotion(x.split())#Option7--> les ""
        x=quotation_between_named_entities(x,named_entities)
        #x=order_by_named_entities(x,named_entities)
        #lst=seg.split_accourding_numbers(x)
        for item in x:
            try:
                item=item.decode('utf8')
            except Exception as e:
                pass
            item=unicodedata.normalize('NFKD',item)
            item_query = similar_word(model,x,item,named_entities,central_words)

            if item_query!='':
                query_final.append(item_query)
        rank+=1
        print ("D AR AR "+str(rank).zfill(4)+" "+u'+'.join(query_final))
        query_global.append(("D AR AR "+str(rank).zfill(4)+" "+u' '.join(query_final)))
    return '\n'.join(query_global)
def tsne_plot(model):
	"Creates and TSNE model and plots it"
	labels = []
	tokens = []

	for word in model.wv.vocab:
		tokens.append(model[word])
		labels.append(word)
    
	tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
	new_values = tsne_model.fit_transform(tokens)

	x = []
	y = []
	for value in new_values:
		x.append(value[0])
		y.append(value[1])
        
	plt.figure(figsize=(16, 16)) 
	for i in range(len(x)):
		plt.scatter(x[i],y[i])
		plt.annotate(labels[i],
					xy=(x[i], y[i]),
					xytext=(5, 2),
					textcoords='offset points',
					ha='right',
					va='bottom')
	plt.show()

if __name__=="__main__":
	
    #path of files
    path_Q="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/benajiba/ArabicQuestionss"
    path_named_entity="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/benajiba/named_entity"
    path_central_words="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/benajiba/word_cetrale_secondaire.txt"
    path_stop_word="/media/rmimez/8A1CED061CECEE5F/etude/soutenance_M2/word2vec/programs/essayer/benajiba/stop_words.txt"

    #read list of named entities
    lst_named_entities=open(path_named_entity,'r').read().split()
    lst_named_entities=[item.decode('utf8') for item in lst_named_entities]
    lst_named_entities=[unicodedata.normalize('NFKD',item) for item in lst_named_entities]



    #read list of central_words
    central_words=open(path_central_words,'r').read().split()
    central_words=[item.decode('utf8') for item in central_words]
    central_words=[unicodedata.normalize('NFKD',item) for item in central_words]
    central_words=[clean_str(item) for item in central_words]

    #load the model
    new_model1 = models.Word2Vec.load('/home/rmimez/Documents/dataset/models/wiki_cbow_300/wikipedia_cbow_300')
    new_model2 = models.Word2Vec.load('/home/rmimez/Documents/dataset/models/wiki_sg_300/wikipedia_sg_300')

    #export queries as list of type string
    lst=queries(new_model1,read_Q_data(path_Q),lst_named_entities,central_words)
    lst1=queries(new_model2,read_Q_data(path_Q),lst_named_entities,central_words)

    #write queries in file
    file('search_results/result final7/google_results4/CBOW_quiries.txt','w').write(lst.encode('utf8'))
    file('search_results/result final7/google_results4/SKIP_GRAM_quiries.txt','w').write(lst1.encode('utf8'))

