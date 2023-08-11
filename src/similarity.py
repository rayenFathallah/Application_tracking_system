import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Convert job description and resume to binary vectors

def vectorize_features(features, feature_list):
    vector = [1 if feature in features else 0 for feature in feature_list]
    return vector
def match_profile(job_description,resume) : 
# Combine all features from job description and resume
    #all_features = list(set(job_description['skills'] + job_description['education'] + job_description['experience'] + resume['skills'] + resume['education'] + resume['experience']))

    #job_vector = vectorize_features(job_description['skills'] + job_description['education'] + job_description['experience'], all_features)
    #resume_vector = vectorize_features(resume['skills'] + resume['education'] + resume['experience'], all_features)
    all_skills = list(set(job_description["SKILLS"]+resume['skills']))  
    job_vector = vectorize_features(job_description['SKILLS'], all_skills)
    resume_vector = vectorize_features(resume['skills'] , all_skills)
    # Calculate cosine similarity
    cosine_sim = cosine_similarity([job_vector], [resume_vector])[0][0]
    print(f'jd skills : {job_description["SKILLS"]}')   
    print(f'profile skills : {resume["skills"]}')             
    print(f"Cosine Similarity: {cosine_sim}")
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
        return 0 
