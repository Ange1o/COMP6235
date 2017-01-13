from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup
import csv
import json
import pandas
from pymongo import MongoClient
import nltk
import yaml
from pprint import pprint
from collections import OrderedDict
from urllib.error import HTTPError

# mongodb conection
user = 'group'
password = '1234'
uri="mongodb://localhost"
client = MongoClient(uri)
db = client.trends10
coll = db.fish_trend

#import files
csvfile = open('/home/user/main/GroupC/potato_trendExport_V1.csv','r')
reader = csv.DictReader( csvfile )
header = ["Date","Month","Year","keyword","rising","query_result_title","query_result_link","query_result_des","top_query_id"]
for each in reader:
    row={}
    for field in header:
        row[field]=each[field]
        
    coll.insert_one(row)
	
#get content from webpages
c = coll.find({"query_result_link":{'$ne':""}},{"query_result_link":True,"_id":True})
a=list(c)
for i in a:
    site = i["query_result_link"]
    id1=i['_id']
    try:
        fp = urllib.request.urlopen(site)
    except HTTPError:
        print ('HTTP Error')
        print (site)
        continue
    try:
        a = fp.read()
    except ConnectionResetError:
        print('Connection Reset')
        print(site)
        fp = urllib.request.urlopen(site)
        a = fp.read()

    b = BeautifulSoup(a,"html.parser")
    s = b.find_all('p')
    t = ""
    for i in s:
        t=t+i.get_text() 
        d={"query_result_content":t}
    coll.update_one({"_id": id1},{'$set':{"query_result_content":t}})

def nl_analyze(text, Factors, Type):
        # tokenize the sentenses，split into sentences
        sentence_splitter = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
        sentences_list = sentence_splitter.tokenize(text)
        nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()
        tokenized_sentences = [nltk_tokenizer.tokenize(sent) for sent in sentences_list]

        
        #tag the words
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        pos_tagged_sentences = [[(word, [postag]) for (word, postag) in sentence] for sentence in tagged_sentences]

        
        # import the dictionaries
        dictionary_paths = [ '/home/user/main/GroupC/recipe.yml', '/home/user/main/GroupC/pollution.yml', '/home/user/main/GroupC/quality.yml','/home/user/main/GroupC/cost.yml','/home/user/main/GroupC/disease.yml']
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        myDictionary = {}
        max_phrase_size = 0 # the longest length of the phrases in dictionary
        for curr_dict in dictionaries:
            for phrase in curr_dict:
                if phrase in myDictionary:
                    # dictionary[key] is a list. Attent the properties
                    myDictionary[phrase].extend(curr_dict[phrase])
                else:
                    myDictionary[phrase] = curr_dict[phrase]
                    max_phrase_size = max(max_phrase_size, len(phrase.split()))

        # tag sentences through dictionary
        dic_tagged_sentences = []
        for sentence in pos_tagged_sentences:
            dic_tagged_sen = []
            N = len(sentence)
            if max_phrase_size == 0:
                max_phrase_size = N
            i =0 # the start place of the sentence
            while(i<N):
                j = min(i+max_phrase_size, N) # the current place of the sentence
                tagged = 0
                while(i<j): 
                    expression = ' '.join([word[0] for word in sentence[i:j]]).lower()
                    if expression in myDictionary:
                        original_position = i
                        is_single = j-i
                        i=j
                        taggings = [tags for tags in myDictionary[expression]]
                        tagged_expression = (expression, taggings)
                        if (is_single) :
                            original_taggings = sentence[original_position][1]
                            tagged_expression[1].extend(original_taggings)
                        dic_tagged_sen.append(tagged_expression)
                        tagged = 1
                    else:
                        j = j-1
                if not tagged:
                    dic_tagged_sen.append(sentence[i])
                    i += 1
            dic_tagged_sentences.append(dic_tagged_sen)

        #calculate the scores
        Count_Factors = {}
        Count_Type = {"positive":0,"negative":0}
        sorted_Count_Factors = {}
        sorted_Count_Type = {}
        for sentence in dic_tagged_sentences:
            for word in sentence:
                for tag in word[1]:
                    if tag in Factors:
                        Count_Factors[tag] = Count_Factors.get(tag,0)+1.0
                    elif tag in Type:
                        Count_Type[tag] =Count_Type.get(tag,0)+1.0
        
        sorted_Count_Factors = OrderedDict(sorted(Count_Factors.items(), key=lambda x: x[1], reverse=True))
        sorted_Count_Type = OrderedDict(sorted(Count_Type.items(), key=lambda x: x[1], reverse=True))
		
		# test printing
        print(Count_Factors, Count_Type)
        Content ={"Factors":sorted_Count_Factors,"Type":sorted_Count_Type}
        print("Content:")
        pprint(Content)
        

        # calculate factor
        i = 10
        top_c = 0
        top_key = ""
        score = 0
        if len(Count_Factors) == 0:
            result = {"none":1}
        else: 
            for key,c in sorted_Count_Factors.items():
                if i == 0:
                    break
                if i == 10:
                    top_key = key
                    top_c = 1.0*c
                    score += top_c
                else:
                    score += 1.0*c
                i -= 2
            re = top_c/score*100.00
            result = {top_key:re}
    
        #calculate type
        if len(sorted_Count_Type) == 0:
            top_key = "neutral"
        else:
            i = 1
            for t, v in sorted_Count_Type.items():
                if i == 1:
                    top_key = t
                    break
        re = Count_Type["positive"]-Count_Type["negative"]
        result.update({top_key:re})
        return result

def result_update(old,new,key):
    if key in old.keys():
        for i in new:
            old[key][i] = old[key].get(i,0)+new[i]
    else:
        old[key] = new
    return old

#to summarize the ten contents for each query keyword
def result_summary(result,Factors,Type):
    ordered_dic = {}
    fin_result = {}
    for i in result:
        ordered_dic = OrderedDict(sorted(result[i].items(), key=lambda x: x[1], reverse=True))
        f_flag = 2
        t_flag = 1
        t_total = 0
        f_total = 0
        top_key = ""
        top_kry_t = ""
        top_v = 0
        re = 0
        re_t = 0  
        
        for k,v in ordered_dic.items():
            if k in Factors:
                if f_flag:
                    if f_flag == 2:
                        top_key = top_key+k
                    if f_flag == 1:
                        top_key = top_key+","+k
                    top_v += v
                    f_flag -=1
                    f_total += v
                else:
                    f_total += v
                re = top_v/f_total*100.00
                    
            if k in Type:
                t_total += v
                re_t = t_total
                
        if t_total > 0:
            top_key_t = "positive"
        elif t_total == 0:
            top_key_t = "neutral"
        else:
            top_key_t = "negative"
			
        fin_result.update({i:{top_key_t:re_t}})
        fin_result[i].update({top_key:re})
    return fin_result

#analyze the content
coll = db.fish_trend
c = coll.find({"query_result_content":{"$exists":True}})
cl = c
result_keyword_dic = {}
Factors = ["disaster","pollution","cost","recipe","weather","events","product","quality","none"]
Type = ["positive","negative","neutral"]   
for i in cl:
    keyword = i['keyword']
    id_1 = i['_id']
    result_content_dic = nl_analyze(i['query_result_content'],Factors,Type)
    result_keyword_dic = result_update(result_keyword_dic,result_content_dic,keyword)
result_to_insert = result_summary(result_keyword_dic,Factors,Type)

#insert result to database
for i in result_to_insert:
    a = result_to_insert[i]
    re = {}
    for k in a: #adapt the format to store in database
        if k in Type:
            types = {"type":k,"type_score":a[k]}
        else:
            factors = {'factor':k,"factor_score":a[k]}
    re.update(factors)
    re.update(types)
    coll.update_many({"keyword": i},{'$set':re})
    
c = coll.find({"query_result_content":{"$exists":True}},{"query_result_content":False})
cl = list(c)



