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
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from src.data_preprocessing.resume_preprocessing import extract_all_info
from src.data_ingestion.data_exporter import export_data_json
from src.data_preprocessing.job_description_preprocessing import get_jd_info
from src.similarity import match_profile,overall_similarity,similarity_aggreg,tf_idf_vectorizing
from concurrent.futures import ThreadPoolExecutor

def process_lines(resume,data_scientist_jd,skill_extractor,skills_model,model_80_resume,model_150_jd) : 
    ''' 
    function that runs 4 processes in parallel
    '''
    res=extract_all_info(resume['content'],skill_extractor,skills_model)
    jd_info = get_jd_info(data_scientist_jd,skill_extractor,skills_model)
    tf_sim = tf_idf_vectorizing(data_scientist_jd,resume['content'])
    overall = overall_similarity(data_scientist_jd,elem['content'],model_80_resume,model_150_jd)

    return {'res':res,'jd_info': jd_info, 'tf_sim':tf_sim,'overall':overall}


tika.initVM()
file_names = os.listdir('./data/test_data/final_test')
path = 'data/test_data/final_test'
resumes_list = read_files(file_names,path)
infos_results_final = list()
nlp = spacy.load("en_core_web_lg")
skills_model = spacy.load('models/model-best')
    # init skill extractor
data_scientist_jd="Programming Skills – knowledge of statistical programming languages like R, Python, and database query languages like SQL, Hive, Pig is desirable. Familiarity with Scala, Java, or C++ is an added advantage. Statistics – Good applied statistical skills, including knowledge of statistical tests, distributions, regression, maximum likelihood estimators, etc. Proficiency in statistics is essential for data-driven companies. Machine Learning – good knowledge of machine learning methods like k-Nearest Neighbors, Naive Bayes, SVM, Decision Forests. Strong Math Skills (Multivariable Calculus and Linear Algebra) - understanding the fundamentals of Multivariable Calculus and Linear Algebra is important as they form the basis of a lot of predictive performance or algorithm optimization techniques. Data Wrangling – proficiency in handling imperfections in data is an important aspect of a data scientist job description. Experience with Data Visualization Tools like matplotlib, ggplot, d3.js., Tableau that help to visually encode data Excellent Communication Skills – it is incredibly important to describe findings to a technical and non-technical audience. Strong Software Engineering Background Hands-on experience with data science tools Problem-solving aptitude Analytical mind and great business sense Degree in Computer Science, Engineering or relevant field is preferred Proven Experience as Data Analyst or Data Scientist"
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
weights = {'skills':100,'niveau':0,'experience':0}
model_weights = {'overall' : 0.4,'info':0.4,'tf_idf':0.2}
model_150_jd = Doc2Vec.load('resumes_model_epochs_lemmetized_150.model')
model_80_resume = Doc2Vec.load('resumes_model_epochs_lemmetized_80.model')
results = list()

with ThreadPoolExecutor(max_workers=4) as executor:

    for elem in resumes_list : 
        future = executor.submit(process_lines, elem,data_scientist_jd, skill_extractor, skills_model,model_80_resume,model_150_jd)
        info = match_profile(future.result()['jd_info'],future.result()['res'],weights) 
        final_result = similarity_aggreg(future.result()['overall'],info,future.result()['tf_sim'],model_weights)
        results.append({'name':elem['name'],'similarity_agg':final_result,'skills_sim':info})
print(results)
