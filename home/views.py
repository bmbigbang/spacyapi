from django.shortcuts import render
from django.http import HttpResponse
import spacy,numpy,os,json,urllib,operator
from math import exp
from spacy.en import English, LOCAL_DATA_DIR
data_dir = os.environ.get('SPACY_DATA',LOCAL_DATA_DIR)
try:
	sethaeh = nlp(unicode('s'))
except:
	nlp=English(data_dir=data_dir)

def tokenizer(request):
    q = request.get_full_path()
    p = urllib.unquote_plus((q.replace("/api/tokenizer/","")))
    doc=nlp(unicode(p));types={};entities=[];tokenizer=[];dicfin={}
    for token in doc:
	tokenizer.append(str(token.orth_))
        if str(token.pos_) in types:
	    types[token.pos_].append(str(token.orth_))
        else:
            types[token.pos_]=[str(token.orth_)]
    for ents in doc.ents:
        entities.append([str(ents.orth_),str(ents.label_)])

    dicfin = {'tokens':tokenizer,'entities':entities,'types':types}
    return HttpResponse(json.dumps(dicfin))

def similarity(request):
    q = request.get_full_path()
    p = urllib.unquote_plus((q.replace("/api/similarity/","")))
    p = p.split("&")
    doc = nlp(unicode(p[0])); res = {}
    if len(p)>1:
	doc2 = nlp(unicode(p[1]))
    else:
        doc2 = nlp(unicode(p[0]))
    for i in doc:
        if str(i.orth_) in res:
            continue
        for j in doc2:
            if str(i.pos_)!='PUNCT' and str(j.pos_)!='PUNCT':
                if str(i.pos_)!='NUM' and str(j.pos_)!='NUM' and i.orth_!=j.orth_:
                    if str(i.orth_) in res:
                        res[str(i.orth_)].append([str(j.orth_),i.similarity(j)])
                    else:
                        res[str(i.orth_)]=[[str(j.orth_),i.similarity(j)]]
    return HttpResponse(json.dumps(res))

def lemma(request):
    q = request.get_full_path()
    p = urllib.unquote_plus((q.replace("/api/lemma/","")))
    res = []; doc = nlp(unicode(p))
    for token in doc:
        try:
            res.append([token.orth_,token.lemma_])
        except:
            res.append([token.orth_,""])
    return HttpResponse(json.dumps(res))

def vector(request):
    q = request.get_full_path()
    p = urllib.unquote_plus((q.replace("/api/vector/","")))
    res= {}; doc = nlp(unicode(p))
    for token in doc:
	vector = []
	for i in token.vector:
	    vector.append(str(i))
	res[token.orth_] = vector
    return HttpResponse(json.dumps(res))

def filter(request):
    q = request.get_full_path()
    p = urllib.unquote_plus((q.replace("/api/filter/",""))).replace("&"," ")
    temp = numpy.zeros(300); doc = nlp(unicode(p)); a = doc[0].vector; f = doc[1].vector
    dictionary = {"food":["italian","pizza","bacon","mexican","chinese","japanese",
                "barbeque","vietnamese","food","takeaway","delivery",
                 "restaraunt","cafe","vegetarian","lebanese","indian","menu",
                 "thai","indonesian","grill","bar","french","seafood","vegan"]}
    c = dictionary[str(doc[2].orth_)]
    for j in c:
        b = nlp(unicode(j))[0].vector
        for i in range(len(a)):        
            if a[i]*b[i] >= 2.0/300:
                temp[i] += ( (a[i]*b[i])*exp(2**2)/300**2 )
            elif a[i]*b[i] >= 1.0/300:
                temp[i] += ( (a[i]*b[i])*exp(3**2)/300**2 )    
            elif a[i]*b[i] >= 0.5/300:
                temp[i] += ( (a[i]*b[i])*exp(4**2)/300**2 )
            elif a[i]*b[i] >= -2.0/300:
                temp[i] += ( (a[i]*b[i])*exp(5**2)/300**2 )
            elif a[i]*b[i] <= -1.0/300:
                temp[i] += ( (a[i]*b[i])*exp(0.5**2)/300**2 )
            elif a[i]*b[i] <= -0.5/300:
                temp[i] += ( (a[i]*b[i])*exp(0.33**2)/300**2 )
            elif a[i]*b[i] <= -0.1/300:
                temp[i] += ( (a[i]*b[i])*exp(0.25**2)/300**2 )
            else:
                temp[i] += ( (a[i]*b[i])*exp(0.2**2)/300**2 )
    return HttpResponse(unicode(numpy.inner(temp,f)))


# Create your views here.
