import datetime
import time
import sys
import MeCab
import operator
from pymongo import MongoClient
from bson import ObjectId
from itertools import combinations

stop_word={}
DBname="db20171639"
conn=MongoClient('dbpurple.sogang.ac.kr')
db=conn[DBname]
db.authenticate(DBname,DBname)

def printMenu():
    print "0. CopyData"
    print "1. Morph"
    print "2. print morphs"
    print "3. print wordset"
    print "4. frequent item set"
    print "5. association rule"

def make_stop_word():
    f=open("wordList.txt",'r')
    while True:
        line=f.readline()
        if not line: break
        stop_word[line.strip('\n')]=line.strip('\n')
    f.close()

def morphing(content):
    t=MeCab.Tagger('-d/usr/local/lib/mecab/dic/mecab-ko-dic')
    nodes=t.parseToNode(content.encode('utf-8'))
    MorpList=[]
    while nodes:
        if nodes.feature[0]=='N' and nodes.feature[1]=='N':
            w=nodes.surface
            if not w in stop_word:
                try:
                    w=w.encode('utf-8')
                    MorpList.append(w)
                except:
                    pass
        nodes=nodes.next
    return MorpList

def p0():
    """
    copydata news to news_freq
    """
    col1=db['news']
    col2=db['news_freq']
    col2.drop()

    for doc in col1.find():
        contentDic={}
        for key in doc.keys():
            if key!="_id":
                contentDic[key]=doc[key]
        col2.insert(contentDic)
def p1():
    """
    Morph news and update news db
    """
    for doc in db['news_freq'].find():
        doc['morph']=morphing(doc['content'])
        db['news_freq'].update({"_id":doc['_id']},doc)

def p2(url):
    """
    input : news url
    output : news morphs
    """
    for doc in db['news_freq'].find():
        doc['morph']=morphing(doc['content'])
        db['news_freq'].update({"_id":doc['_id']},doc)

        if(doc['url']==url):
            for w in doc['morph']:
               print(w.encode('utf-8'))

def p3():
    """
    copy news morph to new db named news_wordset
    """
    col1=db['news_freq']
    col2=db['news_wordset']
    col2.drop()
    for doc in col1.find():
        new_doc={}
        new_set=set()
        for w in doc['morph']:
            new_set.add(w.encode('utf-8'))
        new_doc['word_set']=list(new_set)
        new_doc['url']=doc['url']
        col2.insert(new_doc)

def p4(url):
    """
    input : news url
    output : news wordset
    """
    col=db['news_wordset']
    col.drop()

    for doc in db['news_freq'].find():
        new_doc={}
        new_set=set()
        for w in doc['morph']:
            new_set.add(w.encode('utf-8'))
        new_doc['word_set']=list(new_set)
        new_doc['url']=doc['url']
        col.insert(new_doc)

    for doc in col.find():
        if(doc['url']==url):
            for w in doc['word_set']:
               print(w.encode('utf-8'))

def p5(length):
    """
    make frequent item_set
    and insert new dbs(dbname=candidate_L+"length")
    """
    min_sup=(db['news'].count())*0.1

    if(length==1):
        #candidate_L1
        item_set=set()
        value_set=set()
        dic={}
        col=db['candidate_L1']
        col.drop()
        for doc in db['news_wordset'].find():
            for w in doc['word_set']:
                dic[w]=0


        for doc in db['news_wordset'].find():
            for w in doc['word_set']:
                dic[w]=dic[w]+1
        for key, value in dic.items():
            if(value<min_sup):
                continue
            else:
                new_doc={}
                new_doc['item_set']=key.encode('utf-8')
                new_doc['support']=value
                col.insert(new_doc)

        
    elif(length==2):
        #candidate_L2
        dic={}
        dic2={}
        col2=db['candidate_L2']
        col2.drop()
        for doc in db['news_wordset'].find():
            for w in doc['word_set']:
                dic[w]=0

        for doc in db['news_wordset'].find():
            for w in doc['word_set']:
                dic[w]=dic[w]+1
        for key,value in dic.items():
            if(value<min_sup):
                dic.pop(key)
        for key1 in dic.keys():
            for key2 in dic.keys():
                if(key1<key2):
                    dic2[key1,key2]=0
                elif(key1>key2):
                    dic2[key2,key1]=0

        for key, value in dic2.items():
            for doc in db['news_wordset'].find():
                for w1 in doc['word_set']:
                    if(w1==key[0]):
                        for w2 in doc['word_set']:
                            if(w2==key[1]):
                                value=value+1
            if(value>=min_sup):
                new_doc={}
                new_doc['item_set']=list(key)
                new_doc['support']=value
                col2.insert(new_doc)

    elif(length==3):
        #candidate_L3
        dic={}
        dic2={}
        dic3={}
        col3=db['candidate_L3']
        col3.drop()
        for doc in db['news_wordset'].find():
            for w in doc['word_set']:
                dic[w]=0

        for doc in db['news_wordset'].find():
            for w in doc['word_set']:
                dic[w]=dic[w]+1
        for key,value in dic.items():
            if(value<min_sup):
                dic.pop(key)

        for key1 in dic.keys():
            for key2 in dic.keys():
                if(key1<key2):
                    dic2[key1,key2]=0
                elif(key1>key2):
                    dic2[key2,key1]=0
        
        for key, value in dic2.items():
            for doc in db['news_wordset'].find():
                for w1 in doc['word_set']:
                    if(w1==key[0]):
                        for w2 in doc['word_set']:
                            if(w2==key[1]):
                                        value=value+1
                
            if(value<min_sup):
                dic2.pop(key)

        for key in dic2.keys():
            for key3 in dic.keys():
                if(key[0]>key3):
                    if(key[1]>key3):
                        dic3[key3,key[0],key[1]]=0
        for key, value in dic3.items():
            for doc in db['news_wordset'].find():
                for w1 in doc['word_set']:
                    if(w1==key[0]):
                        for w2 in doc['word_set']:
                            if(w2==key[1]):
                                for w3 in doc['word_set']:
                                    if(w3==key[2]):
                                        value=value+1
            if(value>=min_sup):
                new_doc={}
                new_doc['item_set']=list(key)
                new_doc['support']=value
                col3.insert(new_doc)
        

def p6(length):
    """
    make strong association rule
    and print all of strong rules
    by length-th frequent item set
    """
#    min_conf=(db['news'].count())*0.5
    min_conf=0.5
    if(length==2):
        col=db['candidate_L2']
        for doc in col.find():
            for i in range(2):
                count_X=0.0
                count_Y=0.0
                X=doc['item_set'][i]
                for doc2 in db['candidate_L1'].find():
                    if(X==doc2['item_set']):
#                    if((X==doc2['item_set'][0])or(X==doc2['item_set'][1])):
                        count_X+=doc2['support']
                for doc3 in col.find():
                    if(doc['item_set']==doc3['item_set']):
                        count_Y+=doc3['support']
                fre=count_Y/count_X
                if(fre>=min_conf):
                    print(doc['item_set'][i]+" =>"+doc['item_set'][(i+1)%2]+" "+(str)(fre))
    elif(length==3):
        col=db['candidate_L3']
        for doc in col.find():
            for i in range(3):
                count_X=0.0
                count_Y=0.0
                X=doc['item_set'][i]
                for doc2 in db['candidate_L1'].find():
                    if(X==doc2['item_set']):
                        count_X+=doc2['support']
                for doc3 in col.find():
                    if(doc['item_set']==doc3['item_set']):
                        count_Y+=doc3['support']
                fre=count_Y/count_X
                if(fre>=min_conf):
                    print(doc['item_set'][i]+" =>"+doc['item_set'][(i+1)%2]+" "+(str)(fre))

        for doc in col.find():
            for i in range(3):
                count_X=0.0
                count_Y=0.0
#                X1=doc['item_set'][i%3]
#                X2=doc['item_set'][(i+1)%3]
                new_set=set()
                new_set.add(doc['item_set'][i%3])
                new_set.add(doc['item_set'][(i+1)%3])
                for doc2 in db['candidate_L2'].find():
                    if(set(doc2['item_set'])==new_set):
#                    if(((X1==doc2['item_set'][0])and(X2==doc2['item_set'][1]))or((X1==doc2['item_set'][1])and(X2==doc2['item_set'][0]))):
                        count_X+=doc2['support']
                for doc3 in col.find():
                    if(doc['item_set']==doc3['item_set']):
                        count_Y+=doc3['support']
                fre=count_Y/count_X
                if(fre>=min_conf):
                    print(doc['item_set'][i]+" =>"+doc['item_set'][(i+1)%2]+" "+(str)(fre))
                    

                        



if __name__ =="__main__":
    make_stop_word()
    printMenu()
    selector=input()
    if selector==0:
        p0()
    elif selector==1:
        p1()
        p3()
    elif selector==2:
        url=str(raw_input("input news url: "))
        p2(url)
    elif selector==3:
        url=str(raw_input("input news url: "))
        p4(url)
    elif selector==4:
        length=int(raw_input("input length of the frequent item:"))
        p5(length)
    elif selector==5:
        length=int(raw_input("input length of the frequent item:"))
        p6(length)
            

