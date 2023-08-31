import pandas as pd 
import spacy 
import tika 
import re
import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from numpy.linalg import norm
from src.data_preprocessing.resume_preprocessing import detect_lang,extract_years_of_experience,remove_accents,detect_niveau_similarity,extract_skills,extract_skills2
def get_jd_info(jd_data_text) :
  dic_jd = {}
  current_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the path to the models directory
  models_dir = os.path.join(current_dir, '../../models/model-best')
  model2 = spacy.load(models_dir)
  dic_jd['after_bac']=[]
  dic_jd['SKILLS']=[]
  jd_data_text=remove_accents(jd_data_text.lower())
  programs = ['licence ', 'cycle ingenieur ','ingenieurie','ingenieur', 'ingenieurie en ', 'master ', 'mastere ','phd','doctorat ','engineering ','engineer ','bachelor ','B.E ','graduate ', 'post-graduate ','pre-engineering ','préparatoire ']
  nlp = spacy.load("en_core_web_lg")
  after_bac_pattern = r'\b(?:bac|baccalaureat)\s*\+\s*(\d+)\b'
  matches_bac = re.findall(after_bac_pattern, jd_data_text, re.IGNORECASE)
  pattern_niveau = r'\b(?:' + '|'.join(re.escape(word) for word in programs) + r')\b'
  program_matches = re.findall(pattern_niveau, jd_data_text, re.DOTALL)
  #### Loading the model is slow ==> has to be done only once 
  new_jd = detect_lang(jd_data_text)
  program_matches2 = re.findall(pattern_niveau, jd_data_text, re.DOTALL)
  final_program= set(program_matches+program_matches2) 
  label_list_jd=list()
  text_list_jd = list()
  #doc_jd = jd_model(new_jd)
  dic_jd['SKILLS'] = list(set(extract_skills2(jd_data_text,model2)))
  ''' 
  for ent in doc_jd.ents:
      label_list_jd.append(ent.label_)
      text_list_jd.append(ent.text)
  for index in range(len(label_list_jd)) : 
      if label_list_jd[index] in dic_jd.keys() : 
          dic_jd[label_list_jd[index]].append(text_list_jd[index])
      else : 
          dic_jd[label_list_jd[index]] = [text_list_jd[index]]
'''
  dic_jd['program_details'] = list(final_program)
  dic_jd['Year_experience'] = extract_years_of_experience(jd_data_text)
  niveauu = get_niveau(jd_data_text) 
  if len(matches_bac) > 0 : 
    dic_jd['after_bac'] = detect_niveau(matches_bac[0]) 
  else : 
      dic_jd['after_bac'] = ['0']
  dic_jd['exact_niveau'] = detect_niveau(dic_jd['after_bac'],niveauu)

  return dic_jd
def get_niveau(resume_text) : 

    niveau = ['licence ', 'cycle ingenieur ', 'ingenieurie en ', 'master ', 'mastère ','phd','doctorat ','engineering ','engineer ','bachelor ','B.E ', 'post-graduate ','pre-engineering ','preparatoire ','prepa']
    pattern_niveau = r'\b(?:' + '|'.join(re.escape(word) for word in niveau) + r')\b'
    # Use the regular expression to find all matching words in the text
    matching_niveau = set(re.findall(pattern_niveau, resume_text, re.IGNORECASE))
    if len(matching_niveau) > 0 : 

        return list(matching_niveau)
    else :
        return []
def detect_niveau(years_after_bac,niveau) : 
    matching_dic = { 
        '3' : ['licence'], 
        '5' : ['ingernieurie','mastere'],
        '6' : ['ingenieurie','mastere'],
        '9' : ['doctorat']
    }
    if str(years_after_bac) in matching_dic.keys() : 
        return matching_dic[str(years_after_bac)]
    else : 
        return detect_niveau_similarity(niveau)
# second model building ( this one captures semantic similarity in a whole document)
def job_preprocessing(job_description) : 
    jd_data = pd.read_csv('/data/jobs_data/JobsDataset.csv') 
    jd_data.drop(['ID','Query'], axis=1, inplace=True)
    jd_data['data'] = jd_data[['Job Title','Description']].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    tagged_data = [TaggedDocument(words = word_tokenize(_d.lower()), tags = [str(i)]) for i, _d in enumerate(jd_data)]
    model = Doc2Vec(vector_size = 50,
    min_count = 5,
    epochs = 100,
    alpha = 0.001
    )
    model.build_vocab(tagged_data)
    # Get the vocabulary keys
    keys = model.wv.key_to_index.keys()
    # Print the length of the vocabulary keys
    print(len(keys))
    for epoch in range(model.epochs):
        print(f"Training epoch {epoch+1}/{model.epochs}")
        model.train(tagged_data, 
                    total_examples=model.corpus_count, 
                    epochs=model.epochs)

    model.save('cv_job_maching.model')
    print("Model saved")