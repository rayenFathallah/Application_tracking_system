from src.data_ingestion.file_reader import read_files
import tika
import pandas as pd
import os
import spacy
from src.similarity import get_final_similarity
from src.data_preprocessing.resume_preprocessing import extract_education,extract_email,extract_number,extract_skills2
from src.data_preprocessing.job_description_preprocessing import get_jd_info
tika.initVM()
nlp = spacy.load("en_core_web_lg")
#skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
skills_model = spacy.load('models/model-best')
file_names = os.listdir('./data/test_data')
path = 'data/test_data'
weights = {'skills':100,'niveau':0,'experience':0}
data_scientist_jd="Programming Skills – knowledge of statistical programming languages like R, Python, and database query languages like SQL, Hive, Pig is desirable. Familiarity with Scala, Java, or C++ is an added advantage. Statistics – Good applied statistical skills, including knowledge of statistical tests, distributions, regression, maximum likelihood estimators, etc. Proficiency in statistics is essential for data-driven companies. Machine Learning – good knowledge of machine learning methods like k-Nearest Neighbors, Naive Bayes, SVM, Decision Forests. Strong Math Skills (Multivariable Calculus and Linear Algebra) - understanding the fundamentals of Multivariable Calculus and Linear Algebra is important as they form the basis of a lot of predictive performance or algorithm optimization techniques. Data Wrangling – proficiency in handling imperfections in data is an important aspect of a data scientist job description. Experience with Data Visualization Tools like matplotlib, ggplot, d3.js., Tableau that help to visually encode data Excellent Communication Skills – it is incredibly important to describe findings to a technical and non-technical audience. Strong Software Engineering Background Hands-on experience with data science tools Problem-solving aptitude Analytical mind and great business sense Degree in Computer Science, Engineering or relevant field is preferred Proven Experience as Data Analyst or Data Scientist"
resumes_list = read_files(file_names,path)
data_jd = get_jd_info(data_scientist_jd)
for elem in resumes_list :
    print(get_final_similarity(data_jd,elem['content']))


