'''from src.data_ingestion.file_reader import read_files, read_file
import os
import nltk
import time
import pandas as pd 
import spacy 
import tika 

nlp = spacy.load("en_core_web_lg")
jd_data = pd.read_csv('data/jobs_data/JobsDataset.csv')
jd_data_list = jd_data['Description']
jd_model = spacy.load('src/JdModel/output/model-best')
#### Loading the model is slow ==> has to be done only once 
label_list_jd=list()
text_list_jd = list()
dic_jd = {}

doc_jd = jd_model(jd_data_list[2])
for ent in doc_jd.ents:
    label_list_jd.append(ent.label_)
    text_list_jd.append(ent.text)
for index in range(len(label_list_jd)) : 
    if label_list_jd[index] in dic_jd.keys() : 
        dic_jd[label_list_jd[index]].append(text_list_jd[index])
    else : 
        dic_jd[label_list_jd[index]] = [text_list_jd[index]]
print(dic_jd)
''' 
import pandas as pd 
import spacy 
from src.data_ingestion.file_reader import read_files 
from src.data_preprocessing.resume_preprocessing import extract_skills2,extract_all_info
from src.data_ingestion.data_exporter import export_data_json
import tika 
import time
import os 
start_time = time.time()
tika.initVM()
file_names = os.listdir('./data/raw_data')
path = 'data/raw_data'
resumes_list = read_files(file_names,path)
infos_results_final = list()
#jd_data = pd.read_csv('data/jobs_data/JobsDataset.csv')
#jd_data_list = jd_data['Description']
#print(get_jd_info (jd_data_list[1]))
resume_model = spacy.load('src/jdModel/output/model-best')
for elem in resumes_list : 
    res = dict()
    res=extract_all_info(elem,resume_model)
    infos_results_final.append(res)
export_data_json(infos_results_final,'cleaned_data_skills.json')
end_time = time.time()
print("Execution time: {} seconds".format(end_time - start_time))

