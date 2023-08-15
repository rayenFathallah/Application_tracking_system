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
from src.data_preprocessing.job_description_preprocessing import get_jd_info
from src.similarity import match_profile,overall_similarity,similarity_aggreg
tika.initVM()
file_names = os.listdir('./data/test_data')
path = 'data/test_data'
start_time = time.time()
resumes_list = read_files(file_names,path)
infos_results_final = list()
#print(len(resumes_list))
#resumes_list = read_files(['CV_Fadi_Zaafrane.pdf',"experience.pdf"],path)
nlp = spacy.load("en_core_web_lg")
    # init skill extractor
jd_react1 = "Job Description We are looking for a React Native developer interested in building performant mobile apps on both the iOS and Android platforms. You will be responsible for architecting and building these applications, as well as coordinating with the teams responsible for other layers of the product infrastructure. Building a product is a highly collaborative effort, and as such, a strong team player with a commitment to perfection is required. Responsibilities Build pixel-perfect, buttery smooth UIs across both mobile platforms. Leverage native APIs for deep integrations with both platforms. Diagnose and fix bugs and performance bottlenecks for performance that feels native. Reach out to the open source community to encourage and help implement mission-critical software fixes—React Native moves fast and often breaks things. Maintain code and write automated tests to ensure the product is of the highest quality. Transition existing React web apps to React Native.Skills Firm grasp of the JavaScript and TypeScript or ClojureScript language and its nuances, including ES6+ syntax Knowledge of functional or object-oriented programming Ability to write well-documented, clean Javascript code Rock solid at working with third-party dependencies and debugging dependency conflicts Familiarity with native build tools, like XCode, Gradle Android Studio, IntelliJ Understanding of REST APIs, the document request model, and offline storage Experience with automated testing suites, like Jest or Mocha Make sure to mention any other frameworks, libraries, or other technologies relevant to your project List any education level or certification you may require"
jd_react2 = "Your main responsibilities will include: Designing, deploying, and managing web and mobile applications that can run on multiple platforms Utilizing React Native to design and develop UI components for web and mobile apps based on JavaScript Writing effective, scalable, and reusable JavaScript code can help create interchangeable front-end modules Improving front-end performance by diagnosing and fixing all system errors and bugs Using other JavaScript libraries (like “Redux”) to make asynchronous API calls and enhance website/mobile app performance Creating plans to transition React-based web and mobile apps to React Native Planning the data and presentation layer for the front end of all applications Collaborating with design, development, and customer service teams to properly understand client requirements and build top-notch apps within the stipulated time and budget Key Requirements You hold a Bachelor’s degree in Computer Science, Computer/Management Information Systems, Information Technology, Software Engineering, or an associated field You possess at least 4 years of hands-on experience as a React Native Engineer or in a similar role You have a good working knowledge of HTML and CSS You are well-versed in all aspects of JavaScript You have in-depth knowledge of UI/UX designs and wireframes You possess an expert-level understanding of React.js and its fundamentals You are familiar with Gradle, XCode, and other native build tools You have experience working with automated testing suites like Mocha, Jest, etc You deeply understand REST APIs, offline storage, and the document request model You have strong problem-solving and critical-thinking abilities You possess excellent communication skills that facilitate interaction with multiple stakeholders You are confident, detail-oriented, and highly motivated to contribute to the organization's growth as part of a high-performing team You have the ability to work under pressure and adhere to tight deadlines"
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
weights = {'skills':70,'niveau':30,'experience':0}
jd_info = get_jd_info(jd_react2,skill_extractor)
model_weights = {'overall' : 0.5,'info':0.5}
for elem in resumes_list : 
    res = dict()
    print(f"working on {elem['name']} file ...")
    res=extract_all_info(elem['content'],skill_extractor)
    print(res)
    overall = overall_similarity(jd_react2,elem['content'])
    info = match_profile(jd_info,res,weights) 
    print(f'aggregated similarity for {elem["name"]} file : {similarity_aggreg(overall,info,model_weights)}')

#print("Execution time: {} seconds".format(end_time - start_time))
