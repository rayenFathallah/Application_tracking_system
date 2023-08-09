from src.data_ingestion.file_reader import read_files, read_file
import os
import nltk
import time
import spacy 
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import tika 
import pandas as pd
from src.data_preprocessing.resume_preprocessing import extract_all_info
from src.data_ingestion.data_exporter import export_data_json
from src.data_preprocessing.job_description_preprocessing import get_all_skills_jd
tika.initVM()
file_names = os.listdir('./data/raw_data')
path = 'data/raw_data'
start_time = time.time()
#resumes_list = read_files(file_names,path)
infos_results_final = list()
#print(len(resumes_list))
resumes_list = read_files(['CV_Fadi_Zaafrane.pdf',"experience.pdf"],path)
nlp = spacy.load("en_core_web_lg")
    # init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
for elem in resumes_list : 
    res = dict()
    res=extract_all_info(elem,skill_extractor)
    infos_results_final.append(res)

export_data_json(infos_results_final,'cleaned_data_skills.json')
end_time = time.time()

'''jd_data = pd.read_csv('data/jobs_data/JobsDataset.csv')
jd_skills = get_all_skills_jd(jd_data.head(20)['Description'].to_list())
export_data_json(jd_skills,'jd_cleaned.json')
''' 
end_time = time.time()
print("Execution time: {} seconds".format(end_time - start_time))