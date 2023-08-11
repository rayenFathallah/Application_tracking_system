
import pandas as pd 
import spacy 
from src.data_ingestion.file_reader import read_files,read_file
from src.data_preprocessing.resume_preprocessing import extract_skills2,extract_all_info
from src.data_ingestion.data_exporter import export_data_json
from src.data_preprocessing.job_description_preprocessing import get_jd_info
import tika 
from src.similarity import match_profile
import time
import os  
start_time = time.time()
tika.initVM()
jd_model = spacy.load('src/jdModel/output/model-best')

''' 
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

''' 
path = 'data/raw_data'
text2="OVERALL SUMMARY As a Data Scientist on the Data Science Solutions team, this individual will be responsible for building advance data science and analytical solutions that help HBO better understand and grow its best in class television and film library. bac +5 required The data products this individual develops will have a wide impact across the business, from helping HBO audiences discover new content to finding new hit television shows. The Data Scientist will work closely with engineering teams to ensure that their products and insights are properly moved into a production environment, where they can be used by the wider analytics team to drive business strategies. PRIMARY RESPONSIBILITIES Lead the development of data science solutions that help HBO make smarter content decisions across development, scheduling, marketing, and digital platforms (including HBO NOW, HBO GO and HBO.com) Mine HBO and other third party data to better understand how consumers make their entertainment choices Work with engineering teams to transfer knowledge and processes into production environment REQUIREMENTS Bachelor Degree or MS in quantitative field of study (statistics, operations research etc.) from an accredited institution or extensive work experience Experience applying machine learning in a professional environment. Experience with neural networks, computer vision, or deep learning is a plus Strong background in analytic programming (R, Python) Strong desire to continue to learn and develop as a data scientist Proven technical abilities, but excellent written and verbal communication and presentation skills Proven success when partnering with engineering and business teams Logical thinking ability Capability to work on multiple projects simultaneously with limited supervision 4+ years of relevant experience"

scrum_file = read_file('rayen_data.pdf',path)
resume_info=extract_all_info(scrum_file,jd_model)
jd_info = get_jd_info(text2,jd_model)
match_profile(jd_info,resume_info)
