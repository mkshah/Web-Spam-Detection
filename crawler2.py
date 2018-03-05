#Frontier=to store url to be crawled
#Visited=urls crawled
#Discovered=urls discovered on a given webpage

import mechanize
import time
from time import sleep
import MySQLdb
import nltk
from nltk.corpus import stopwords
import re
import string
from gensim import corpora,models,similarities
from nltk.corpus import PlaintextCorpusReader
import os,glob
from numpy import dot
from numpy.linalg import norm


stopWords = stopwords.words('english')             #Stopwords
texts = []
visited_url = []
cluster1 = []
cluster2 = []

def crawl(seeds):

    br = mechanize.Browser()    
#    br.set_proxies({"http":"f2011131:mango@'':8080"})

    br.set_proxies({})
    
    frontier = seeds
    
    filetypes = [".html" , ".php" , ".htm" , ".asp"]

    for crawl_url in frontier:
        if len(visited_url)==5:
            break
        print "Crawling:",crawl_url
        visited_url.append(crawl_url)
        filename = 'text'+str(len(visited_url))
        
        
        try:
            br.open(crawl_url)
            preprocess(br.response().read(),filename)
        except (mechanize.HTTPError,mechanize.URLError) as e:
            print e
            continue

        discovered_url = set()

        for l in br.links():
            for t in filetypes:
                if l.url.endswith(t):
                    if l.url not in frontier and l.url not in visited_url and l.url not in discovered_url:
                        discovered_url.add(l.url)
        
        frontier+=discovered_url
        #print discovered_url,frontier  
        time.sleep(2)
        
    
    
def preprocess(page,filename):
    tokens1 = []
    
    #remove the tags
    raw = nltk.clean_html(page)
    raw = raw.strip().lower().translate(string.maketrans("",""), string.punctuation)
    tokens = raw.split()
    
#    print len(tokens)
    #preprocessing
    for token in tokens:
        if token in stopWords:
            tokens.remove(token)
        elif len(token) <= 4:
            tokens.remove(token)
        elif token.startswith("\\xe"):
            tokens.remove(token)
        else:
            tokens1.append(token)
    tokens = tokens1
#    print 'Tokens length',len(tokens)
    texts.append(tokens)

#    print texts
#    print 'Texts length',len(texts)

def indexing(query):
    #--------------------------------------------------------------------------
    #make dictionary
    #--------------------------------------------------------------------------
    #texts =[['ravi','ravi','programmer'],['linux','good','operating','system'],['ravi','uses','linux']]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('deerwester.dict') # store the dictionary, for future reference
    #print dictionary
    c=len(dictionary)
    #print "\n\n Dictionary to token id\n\n\n"
    #print dictionary.token2id
    #print c
    
    
    #--------------------------------------------------------------------------
    #create Vector space
    #--------------------------------------------------------------------------
    vecSpace = [dictionary.doc2bow(text) for text in texts]
    # doc2bow() simply counts the number of occurences of each distinct word in dictionary, converts the word to its integer word id and returns the result as a sparse vector.
    #http://radimrehurek.com/gensim/tut1.html
    query_1 = dictionary.doc2bow(query.lower().split())
    mm = corpora.MmCorpus.serialize('deerwester.mm', vecSpace) # store to disk, for later use
    print "\n\nVector Space\n\n\n"
    print vecSpace
    
    corpus=corpora.MmCorpus('deerwester.mm')
    #dictionary = corpora.Dictionary.load('deerwester.dict')

    #--------------------------------------------------------------------------
    #create TF-IDF
    #--------------------------------------------------------------------------
    X=list()
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    query_t = tfidf[query_1]
    print "Query 1",query_1,"\n"
    print "Query t",query_t,"\n"
    print "TF-IDF DOCUMENTs\n"
    for doc in corpus_tfidf:
        print doc
        break
    print "\n"
    
    
    #Work on Query

    index = similarities.MatrixSimilarity(corpus_tfidf)
    #print query_t
    #print index
    sims = index[query_t]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print sims,'\n'
    for i in range(0,len(sims)):
        if(sims[i][1]!=0.0):
            print visited_url[sims[i][0]],"\n"
            cluster1.append(visited_url[sims[i][0]])
        else:
            cluster2.append(visited_url[sims[i][0]])

if __name__ == "__main__":
    
    crawl(['http://www.yahoo.com/'])
    query = raw_input("Enter the query:\n")
    print "Your query was:",query
    print "________Searching_____________"
    indexing(query)
    print "____________________________"
    print "Cluster 1",cluster1,"\n\n"
    print "Cluster 2",cluster2,"\n\n"
    



    
