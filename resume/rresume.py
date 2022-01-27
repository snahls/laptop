import warnings
warnings.filterwarnings('ignore')
from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
# from gensim.summarization import summarize,keywords
# from spacy.matcher import PhraseMatcher
import spacy
import os
from pyresparser import ResumeParser
import numpy as np
import pandas as pd
import fitz           #pip install PyMuPDF
import docx2txt

nlp=spacy.load("en_core_web_sm")
app = Flask(__name__)


def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-': #Removing Pronoun
            continue
        result.append(token.lemma_)
    return " ".join(result)


def calculate_similarity(resume_text, job_description):
    base = nlp(resume_text)
    compare = nlp(job_description)
    return base.similarity(compare)


def similartycalc(textlist):
     CountVec=CountVectorizer()
     CountMat=CountVec.fit_transform(textlist)
     Match=cosine_similarity(CountMat)[0][1]
     return Match

def similartytfcalc(textlist):
     Tfidf=TfidfVectorizer()
     CountMat=Tfidf.fit_transform(textlist)
     Match=cosine_similarity(CountMat)[0][1]
     return Match

# def similaritygen(text,jd):
#     matcher=PhraseMatcher(nlp.vocab)
#     try:
#         words=keywords(summarize(jd,word_count=40))
#         patterns=[nlp.make_doc(w) for w in words]
#         matcher.add('Key',patterns)
#         doc=nlp(text)
#         matches=matcher(doc)
#         return len(set(matches))/40
#     except:
#         return 0
                    
@app.route('/')
def html_table():
    return render_template('index1.html')

@app.route('/home', methods=['POST'])
def index():
    if request.method == 'POST':
        job_d = request.form['job']
        path=r'C:\Users\ls59581\Desktop\resume\Resumes'
        dir_list=os.listdir(path+job_d)
        f=open(job_d+"Job.txt", "r")  #The file location is Jupyter_notebook.
        job_text=f.read()
        c=0
        wrong_list=[]
        similar=[]
        relevancy=[]
        resume_list=[]
        path_n=path+job_d
        for i in dir_list:
            new_path=os.path.join(path_n,i) # i is the fileName.
            if (i.split(".")[-2]=='docx') or (i.split(".")[-2]=='pdf'):
                wrong_list.append(new_path)
                c+=1
            else:
                file_format=i.split(".")[-1]
                if file_format=='pdf':
                    pdf=fitz.open(new_path)
                    page_Text=""
                    for page_number in range(pdf.pageCount):
                        page_Text+=pdf.loadPage(page_number).getText('text')
                    processed_data=process_text(page_Text)
                    similarity=calculate_similarity(processed_data,job_text)
                    tfsimilarity= similartytfcalc([processed_data,job_text])
                    csimilarity=similartycalc([processed_data,job_text])
                    #gsimilarity=similaritygen(processed_data,job_text)
                    similar.append("{:.2f}".format(similarity*100))
                    relevancy.append(tfsimilarity+csimilarity)
                    resume_list.append(ResumeParser(new_path).get_extracted_data())
                elif file_format=='docx':
                    page_text = docx2txt.process(new_path)
                    processed_data=process_text(page_text)
                    similarity=calculate_similarity(processed_data,job_text)
                    tfsimilarity= similartytfcalc([processed_data,job_text])
                    csimilarity=similartycalc([processed_data,job_text])
                    #gsimilarity=similaritygen(processed_data,job_text)
                    similar.append("{:.2f}".format(similarity*100))
                    relevancy.append(tfsimilarity+csimilarity)
                    resume_list.append(ResumeParser(new_path).get_extracted_data())
                else:
                    wrong_list.append(new_path)
                    c+=1
            
            df=pd.DataFrame(resume_list)
            df['similarity']=similar
            df['rel']=relevancy
            df['relevance']=0
            dfr=df.sort_values(by='rel', ascending=False)
            dfr.head(10)['relevance']=1
            df=dfr
        df.sort_values(by='similarity', inplace=True, ascending=False)
        df.drop(columns=['college_name', 'no_of_pages', 'rel'], inplace=True)
               

        ranking=df.head(10)['relevance'].values
    
        precision=[]
        for i in range(1,11):
            if ranking[i-1]:
                precision.append(np.sum(ranking[:i])/i)
    
        if precision==[]:
            map1= 0
        map=np.mean(precision)
        

    return render_template('index1.html',wrong_list=wrong_list,map=map, c=c, tables=[df.to_html(classes='data',index=False, header="true")])
        
if __name__ == '__main__':
    app.run(debug=True)