
import pandas as pd 
import spacy 
from src.data_ingestion.file_reader import read_files,read_file
from src.data_preprocessing.resume_preprocessing import extract_skills2,extract_all_info
from src.data_ingestion.data_exporter import export_data_json
from src.data_preprocessing.job_description_preprocessing import get_jd_info
import tika 
from src.similarity import match_profile,overall_similarity,similarity_aggreg
import time
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import os  
start_time = time.time()
tika.initVM()
#jd_model = spacy.load('src/model-best')

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
nlp = spacy.load("en_core_web_lg")
    # init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
path = 'data/raw_data'
jd="We are searching for a Laravel developer to build web applications for our company. In this role, you will design and create projects using Laravel framework and PHP, and assist the team in delivering high-quality web applications, services, and tools for our business. To ensure success as a Laravel developer you should be adept at utilizing Laravel's GUI and be able to design a PHP application from start to finish. A top-notch Laravel developer will be able to leverage their expertise and experience of the framework to independently produce complete solutions in a short turnaround time. Laravel Developer Responsibilities: Discussing project aims with the client and development team. Designing and building web applications using Laravel. Troubleshooting issues in the implementation and debug builds. Working with front-end and back-end developers on projects. Testing functionality for users and the backend. Ensuring that integrations run smoothly. Scaling projects based on client feedback. Recording and reporting on work done in Laravel. Maintaining web-based applications. Presenting work in meetings with clients and management. Laravel Developer Requirements: A degree in programming, computer science, or a related field. Experience working with PHP, performing unit testing, and managing APIs such as REST. A solid understanding of application design using Laravel. Knowledge of database design and querying using SQL. Proficiency in HTML and JavaScript. Practical experience using the MVC architecture. A portfolio of applications and programs to your name. Problem-solving skills and critical mindset. Great communication skills. The desire and ability to learn."
scrum_file = read_file('scrum_master.pdf',path)
overall = overall_similarity(jd,scrum_file)
resume_info = extract_all_info(scrum_file,skill_extractor)
print(resume_info['skills'])
jd_info = get_jd_info(jd,skill_extractor)
print(jd_info['SKILLS'])
print(jd_info['exact_niveau'])
weights = {'skills':70,'niveau':30,'experience':0}
info = match_profile(jd_info,resume_info,weights) 
model_weights = {'overall' : 0.5,'info':0.5}
print(f'aggregated similarity : {similarity_aggreg(overall,info,model_weights)}')
