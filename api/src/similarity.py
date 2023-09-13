import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import string
import re
from src.data_preprocessing.resume_preprocessing import resume_preprocessing_model
weights = {'skills':100,'niveau':0,'experience':0}
model_weights = {'overall' : 0.4,'info':0.4,'tf_idf':0.2}
model_150_jd = Doc2Vec.load('models/resume_models/resumes_model_epochs_lemmetized_150.model')
model_80_resume = Doc2Vec.load('models/resume_models/resumes_model_epochs_lemmetized_80.model')


# Convert job description and resume to binary vectors

def vectorize_features(features, feature_list):
    vector = [1 if feature in features else 0 for feature in feature_list]
    return vector
def find_all_elements(text, list):
  """
  Finds all the elements that exists in the text and the list.

  Args:
    text: The text to search.
    list: The list of elements to search for.

  Returns:
    A list of all the elements that exists in the text and the list.
  """
  results = []
  patterns = [re.compile(element) for element in list]

  for word in text.split():
    for pattern in patterns:
      if pattern.match(word):
        results.append(word)
  return results
def skills_similarity(job_description,resume) : 
# Combine all features from job description and resume
    #all_features = list(set(job_description['skills'] + job_description['education'] + job_description['experience'] + resume['skills'] + resume['education'] + resume['experience']))

    #job_vector = vectorize_features(job_description['skills'] + job_description['education'] + job_description['experience'], all_features)
    #resume_vector = vectorize_features(resume['skills'] + resume['education'] + resume['experience'], all_features)
    added_skills = find_all_elements(resume['text'],job_description)
    all_resume_skills = set(resume['skills']+ added_skills)
    profile_union_jd = list(set(job_description) & set(all_resume_skills))
    all_skills = list(set(job_description))  
    job_vector = vectorize_features(job_description, all_skills)
    resume_vector = vectorize_features(profile_union_jd , all_skills)
    # Calculate cosine similarity
    cosine_sim = cosine_similarity([job_vector], [resume_vector])[0][0]

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
    '''
    Gets information from the job description and the skills, returns the similarity based on defined weights for each section ( skills,education,years of experience)
    '''
    niveau_sim = niveau_similarity(job_description['exact_niveau'],resume['education']['niveau_exacte']) 
    #print(f"niveau in resume {resume['education']['niveau_exacte']}")
    #print(f'niveau similarity {niveau_sim}')
    experience_sim = years_similarity(job_description['Year_experience'],resume['year_of_experience']) 
    #print(f'Experience similarity {experience_sim}')
    if(len(job_description["SKILLS"]) >0) : 

        skills_sim = skills_similarity(job_description['SKILLS'],resume)
    else : 
        skills_sim = 0
    #print(f'skills similarity {skills_sim}')
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
def overall_similarity(job_description,resume,resume_model,jd_model): 
    ## To get an overall similarity of the two documents ( based on semantic similarity not syntax)
    #v1 = model.infer_vector(job_description.split())
    preprocessed_resume = resume_preprocessing_model(resume)
    job_description_vector = jd_model.infer_vector(job_description.split())  # Replace with actual job description tokens
    inferred_vector = resume_model.infer_vector(preprocessed_resume.split())
    #v2 = model.infer_vector(resume.split())
    similarity = 100*(np.dot(np.array(job_description_vector), np.array(inferred_vector))) / (norm(np.array(job_description_vector)) * norm(np.array(inferred_vector)))
    print(f'overall similarity:{round(similarity, 2)}')
    return round(similarity, 2)
def similarity_aggreg(overall_sim,info_sim,tf_idf,weights) : 
    '''Given weights for each layer of similarity, this function returns the final result '''
    sim = (overall_sim * weights['overall'] + info_sim * weights['info']+tf_idf*weights['tf_idf'])
    return sim 
def tf_idf_vectorizing(job_text,resume_text) : 
    ''' 
    tf idf vectorizer returns the counts of the words in a text document, this function returns the similarity between the two vectors 

    ''' 
    job_text_preprocessed = resume_preprocessing_model(job_text)
    resume_preprocessed = resume_preprocessing_model(resume_text)
    vectorizer = TfidfVectorizer()
    tfidf_matrix=vectorizer.fit_transform([resume_preprocessed, job_text_preprocessed])
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    similarity = cosine_sim[0][0]  # Extract the similarity value

    return 100*round(similarity, 2)

def get_final_similarity(job,resume) : 
        tf_sim = tf_idf_vectorizing(job['text'],resume['text'])
        overall = overall_similarity(job['text'],resume['text'],model_80_resume,model_150_jd)
        info = match_profile(job,resume['infos'],weights) 
        final_result = similarity_aggreg(overall,info,tf_sim,model_weights)
    
        return final_result
