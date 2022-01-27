import os
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
#from gensim.summarization import summarize,keywords
#from spacy.matcher import PhraseMatcher
import pandas as pd
import fitz
import docx2txt
from pyresparser import ResumeParser
import spacy
nlp=spacy.load("en_core_web_sm")

add_selectbox = st.sidebar.selectbox(
    "Select Job Description",
    ('DS', 'P')
)

st.subheader('Resume Parser')
folderpath=r'C:\Users\ls59581\Desktop\resume\Resumes'


def file_selector(folder_path=folderpath+add_selectbox):
    file_names = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', file_names)
    return os.path.join(folder_path, selected_filename)
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

#def similaritygen(text,jd):
#   matcher=PhraseMatcher(nlp.vocab)
#    try:
#       words=keywords(summarize(jd,word_count=40))
#       patterns=[nlp.make_doc(w) for w in words]
#       matcher.add('Key',patterns)
#       doc=nlp(text)
#       matches=matcher(doc)
#       return len(set(matches))/40
#    except:
#       return 0

filename = file_selector()
similarity=0
c=0

data = ResumeParser(filename).get_extracted_data()
f=open(add_selectbox+"Job.txt", "r")  #The file location is Jupyter_notebook.
job_text=f.read()
if (filename.split(".")[-2]=='docx') or (filename.split(".")[-2]=='pdf'):
    c+=1
else:
    file_format=filename.split(".")[-1]
    if file_format=='pdf':
        pdf=fitz.open(filename)
        page_Text=""
        for page_number in range(pdf.pageCount):
            page_Text+=pdf.loadPage(page_number).getText('text')
            processed_data=process_text(page_Text)
            similarity=calculate_similarity(processed_data,job_text)
            tfsimilarity=similartytfcalc([processed_data,job_text])
            csimilarity=similartycalc([processed_data,job_text])
           # gsimilarity=similaritygen(processed_data,job_text)
    elif file_format=='docx':
        page_text = docx2txt.process(filename)
        processed_data=process_text(page_text)     
        similarity=calculate_similarity(processed_data,job_text)
        tfsimilarity= similartytfcalc([processed_data,job_text])
        csimilarity=similartycalc([processed_data,job_text])
       # gsimilarity=similaritygen(processed_data,job_text)
    else:
        c+=1
    s=round((similarity+tfsimilarity+csimilarity)*100/3,2)

st.write('Similarity percentage of selected file with selected Job description is`%s`' % s )
df = pd.DataFrame()
df = df.append(data, ignore_index = True)
cols =list(df)
cols.insert(0, cols.pop(cols.index('name')))
df = df.reindex(columns = cols)
st.write(df[cols])

st.subheader('Skills from Resume')
st.table(df['skills'])
st.subheader('Experience from Resume')
st.table(df['experience'])
