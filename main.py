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
tika.initVM()
file_names = os.listdir('./data/raw_data')
path = 'data/raw_data'
start_time = time.time()
resumes_list = read_files(file_names,path)
infos_results_final = list()
#print(len(resumes_list))
nlp = spacy.load("en_core_web_lg")
model2 = spacy.load('models/model-best')
    # init skill extractor
data_scientist_jd="Programming Skills – knowledge of statistical programming languages like R, Python, and database query languages like SQL, Hive, Pig is desirable. Familiarity with Scala, Java, or C++ is an added advantage. Statistics – Good applied statistical skills, including knowledge of statistical tests, distributions, regression, maximum likelihood estimators, etc. Proficiency in statistics is essential for data-driven companies. Machine Learning – good knowledge of machine learning methods like k-Nearest Neighbors, Naive Bayes, SVM, Decision Forests. Strong Math Skills (Multivariable Calculus and Linear Algebra) - understanding the fundamentals of Multivariable Calculus and Linear Algebra is important as they form the basis of a lot of predictive performance or algorithm optimization techniques. Data Wrangling – proficiency in handling imperfections in data is an important aspect of a data scientist job description. Experience with Data Visualization Tools like matplotlib, ggplot, d3.js., Tableau that help to visually encode data Excellent Communication Skills – it is incredibly important to describe findings to a technical and non-technical audience. Strong Software Engineering Background Hands-on experience with data science tools Problem-solving aptitude Analytical mind and great business sense Degree in Computer Science, Engineering or relevant field is preferred Proven Experience as Data Analyst or Data Scientist"
laravel_jd1 = "We are searching for a Laravel developer to build web applications for our company. In this role, you will design and create projects using Laravel framework and PHP, and assist the team in delivering high-quality web applications, services, and tools for our business. To ensure success as a Laravel developer you should be adept at utilizing Laravel's GUI and be able to design a PHP application from start to finish. A top-notch Laravel developer will be able to leverage their expertise and experience of the framework to independently produce complete solutions in a short turnaround time. Laravel Developer Responsibilities: Discussing project aims with the client and development team. Designing and building web applications using Laravel. Troubleshooting issues in the implementation and debug builds. Working with front-end and back-end developers on projects. Testing functionality for users and the backend. Ensuring that integrations run smoothly. Scaling projects based on client feedback. Recording and reporting on work done in Laravel. Maintaining web-based applications. Presenting work in meetings with clients and management. Laravel Developer Requirements: A degree in programming, computer science, or a related field. Experience working with PHP, performing unit testing, and managing APIs such as REST. A solid understanding of application design using Laravel. Knowledge of database design and querying using SQL. Proficiency in HTML and JavaScript. Practical experience using the MVC architecture. A portfolio of applications and programs to your name. Problem-solving skills and critical mindset. Great communication skills. The desire and ability to learn."
laravel_jd2 = "We are seeking a Full Stack Laravel Angular Developer responsible for back-end and front-end development. This position requires a combination of different programming skills (namely PHP, HTML5, CSS3, and JavaScript). The candidate should have a strong understanding of industry trends and content management systems. Also an understanding of the entire web development process, including design, development, and deployment is preferred. The candidate will work with the development team. Therefore, fundamentals on JavaScript frameworks are more than appreciated, and it will allow him to be versatile and to extend any existent tech knowledge in the field. Responsibilities - Designing and implementing new features and functionalities - Developing and customizing plugins - Ensuring high-performance and availability, and managing all technical aspects of Laravel framework. Skills and Qualifications: - Understanding of code versioning tools (git) - Strong understanding of PHP back-end development What else would make stand out? - Basic knowledge with JavaScript frameworks - Good Knowledge of Angular Front End Development"
jd_react1 = "Job Description We are looking for a React Native developer interested in building performant mobile apps on both the iOS and Android platforms. You will be responsible for architecting and building these applications, as well as coordinating with the teams responsible for other layers of the product infrastructure. Building a product is a highly collaborative effort, and as such, a strong team player with a commitment to perfection is required. Responsibilities Build pixel-perfect, buttery smooth UIs across both mobile platforms. Leverage native APIs for deep integrations with both platforms. Diagnose and fix bugs and performance bottlenecks for performance that feels native. Reach out to the open source community to encourage and help implement mission-critical software fixes—React Native moves fast and often breaks things. Maintain code and write automated tests to ensure the product is of the highest quality. Transition existing React web apps to React Native.Skills Firm grasp of the JavaScript and TypeScript or ClojureScript language and its nuances, including ES6+ syntax Knowledge of functional or object-oriented programming Ability to write well-documented, clean Javascript code Rock solid at working with third-party dependencies and debugging dependency conflicts Familiarity with native build tools, like XCode, Gradle Android Studio, IntelliJ Understanding of REST APIs, the document request model, and offline storage Experience with automated testing suites, like Jest or Mocha Make sure to mention any other frameworks, libraries, or other technologies relevant to your project List any education level or certification you may require"
jd_react2 = "Your main responsibilities will include: Designing, deploying, and managing web and mobile applications that can run on multiple platforms Utilizing React Native to design and develop UI components for web and mobile apps based on JavaScript Writing effective, scalable, and reusable JavaScript code can help create interchangeable front-end modules Improving front-end performance by diagnosing and fixing all system errors and bugs Using other JavaScript libraries (like “Redux”) to make asynchronous API calls and enhance website/mobile app performance Creating plans to transition React-based web and mobile apps to React Native Planning the data and presentation layer for the front end of all applications Collaborating with design, development, and customer service teams to properly understand client requirements and build top-notch apps within the stipulated time and budget Key Requirements You hold a Bachelor’s degree in Computer Science, Computer/Management Information Systems, Information Technology, Software Engineering, or an associated field You possess at least 4 years of hands-on experience as a React Native Engineer or in a similar role You have a good working knowledge of HTML and CSS You are well-versed in all aspects of JavaScript You have in-depth knowledge of UI/UX designs and wireframes You possess an expert-level understanding of React.js and its fundamentals You are familiar with Gradle, XCode, and other native build tools You have experience working with automated testing suites like Mocha, Jest, etc You deeply understand REST APIs, offline storage, and the document request model You have strong problem-solving and critical-thinking abilities You possess excellent communication skills that facilitate interaction with multiple stakeholders You are confident, detail-oriented, and highly motivated to contribute to the organization's growth as part of a high-performing team You have the ability to work under pressure and adhere to tight deadlines"
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
weights = {'skills':100,'niveau':0,'experience':0}
model_weights = {'overall' : 0.4,'info':0.4,'tf_idf':0.2}
models = [{'name': 'model80jd','model':Doc2Vec.load('doc2vec_model_epochs_80.model')},
          {'name': 'model100jd','model':Doc2Vec.load('doc2vec_model_epochs_100.model')},
          {'name': 'model150jd','model':Doc2Vec.load('doc2vec_model_epochs_150.model')},
          {'name': 'model40jd','model':Doc2Vec.load('doc2vec_model_epochs_40.model')},
          ]
model_80 = Doc2Vec.load('resumes_model_epochs_lemmetized_80.model')
model_100 = Doc2Vec.load('resumes_model_epochs_lemmetized_100.model')
model_150 = Doc2Vec.load('resumes_model_epochs_lemmetized_150.model')
models_resume = [{'name': 'model80','model':model_80},
          {'name': 'model100','model':model_100},
          {'name': 'model150','model':model_150},

    ]
all_models=models_resume+models
jds= [{'name' : 'react','value' :jd_react1 }, 
      {'name':'data','value':data_scientist_jd}]
i=0
results = list()
for elem in resumes_list : 
    print(f"working on {elem['name']} file ...")
    res = dict()
    res=extract_all_info(elem['content'],skill_extractor,model2)
    for jd in jds : 
        jd_info = get_jd_info(jd['value'],skill_extractor,model2)
        tf_sim = tf_idf_vectorizing(jd['value'],elem['content'])
        info = match_profile(jd_info,res,weights) 
        for jd_model in all_models : 
            for resume_model in all_models : 
                overall = overall_similarity(jd['value'],elem['content'],resume_model['model'],jd_model['model'])
                final_result = similarity_aggreg(overall,info,tf_sim,model_weights)
                results.append({'jd_model':jd_model['name'],'resume_model':resume_model['name'],'type':jd['name'],'name':elem['name'],'similarity':final_result})
df = pd.DataFrame(results) 
#df['ranking']=df.groupby(['type','jd_model','resume_model'])['similarity'].rank(ascending=False)
df.to_csv("perdicted_results_final3.csv")           


#print("Execution time: {} seconds".format(end_time - start_time))
