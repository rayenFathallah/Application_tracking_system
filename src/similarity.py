import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from numpy.linalg import norm
from nltk.corpus import stopwords
import string



# Convert job description and resume to binary vectors

def vectorize_features(features, feature_list):
    vector = [1 if feature in features else 0 for feature in feature_list]
    return vector
def skills_similarity(job_description,resume) : 
# Combine all features from job description and resume
    #all_features = list(set(job_description['skills'] + job_description['education'] + job_description['experience'] + resume['skills'] + resume['education'] + resume['experience']))

    #job_vector = vectorize_features(job_description['skills'] + job_description['education'] + job_description['experience'], all_features)
    #resume_vector = vectorize_features(resume['skills'] + resume['education'] + resume['experience'], all_features)
    profile_union_jd = list(set(job_description) & set(resume))
    all_skills = list(set(job_description))  
    job_vector = vectorize_features(job_description, all_skills)
    resume_vector = vectorize_features(profile_union_jd , all_skills)
    # Calculate cosine similarity
    cosine_sim = cosine_similarity([job_vector], [resume_vector])[0][0]
    print(f'jd skills : {job_description}')   
    print(f'profile skills : {resume}')   
    print(f'intersection : {profile_union_jd}')             
          
    print(f"Cosine Similarity: {cosine_sim}")
    return cosine_sim
    return cosine_sim
def get_similarity(vector1,vector2): 
    return cosine_similarity(vector1,vector2)[0][0]
def years_similarity(job_description_years,resume_years) : 
    if(resume_years!=None) : 
        if(job_description_years <= resume_years) :
    
            return 1 
        else : 
            return resume_years/(job_description_years-resume_years) 
    return 0 
def niveau_similarity(job_description_niveau,resume_niveau) : 
    if len(job_description_niveau) < 1 : 
        return 1 
    else : 
        for elem in resume_niveau : 
            # Same level match
            if elem in job_description_niveau : 
                return 1 
            if 'licence' in job_description_niveau and elem in ['ingenieurie','mastere','doctorat'] : 
            # Higher qualification
                return 1 
        if 'licence' in resume_niveau : 
            return 0.3
        else : 
            # No education detected
            return 0 
def match_profile(job_description,resume,weights) : 
    niveau_sim = niveau_similarity(job_description['exact_niveau'],resume['education']['niveau_exacte']) 
    print(f"niveau in resume {resume['education']['niveau_exacte']}")
    print(f'niveau similarity {niveau_sim}')
    experience_sim = years_similarity(job_description['Year_experience'],resume['year_of_experience']) 
    print(f'Experience similarity {experience_sim}')
    skills_sim = skills_similarity(job_description['SKILLS'],resume['skills'])
    print(f'skills similarity {skills_sim}')
    sim = niveau_sim * weights['niveau'] + experience_sim * weights['experience'] + skills_sim * weights['skills']
    return sim
def preprocess(text):
    stopword_set = set(stopwords.words('english'))
    stopword_set = list(stopword_set)
    stop_words = stopword_set
    #0. split words by whitespace
    text = text.split()
    
    
    # 1. lower case
    text = [word.lower() for word in text]
    
    # 2. remove punctuations
    punc_table = str.maketrans('','',string.punctuation)
    text = [word.translate(punc_table) for word in text]
    
    # 3. remove stop words
    text = [word for word in text if word not in stop_words]
    
    return text
def overall_similarity(job_description,resume): 
    model = Doc2Vec.load('cv_job_maching.model')
    v1 = model.infer_vector(job_description.split())
    v2 = model.infer_vector(resume.split())
    similarity = 100*(np.dot(np.array(v1), np.array(v2))) / (norm(np.array(v1)) * norm(np.array(v2)))
    print(f'overall similarity:{round(similarity, 2)}')
    return round(similarity, 2)
def similarity_aggreg(overall_sim,info_sim,weights) : 
    sim = (overall_sim * weights['overall'] + info_sim * weights['info'])
    print(f'Overall similarity :{overall_sim} \n info similarity : {info_sim} ')
    return sim 
