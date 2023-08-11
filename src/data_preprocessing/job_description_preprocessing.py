import pandas as pd 
import spacy 
import tika 
import re
from src.data_preprocessing.resume_preprocessing import detect_lang,extract_years_of_experience
def get_jd_info(jd_data_text) :
  programs = ['licence ', 'cycle ingenieur ', 'ingenieurie en ', 'master ', 'mastère ', 'diplôme ','phd','diplome','doctorat ','engineering ','engineer ','bachelor ','B.E ','graduate ', 'post-graduate ','pre-engineering ','préparatoire ']
  nlp = spacy.load("en_core_web_lg")
  jd_model = spacy.load('src/JdModel/output/model-best')
  pattern_niveau = r'\b(?:' + '|'.join(re.escape(word) for word in programs) + r')\b'
  program_matches = re.findall(pattern_niveau, jd_data_text, re.DOTALL)
  #### Loading the model is slow ==> has to be done only once 
  new_jd = detect_lang(jd_data_text)
  program_matches2 = re.findall(pattern_niveau, jd_data_text, re.DOTALL)
  final_program= set(program_matches+program_matches2) 
  label_list_jd=list()
  text_list_jd = list()
  dic_jd = {}

  doc_jd = jd_model(new_jd)
  for ent in doc_jd.ents:
      label_list_jd.append(ent.label_)
      text_list_jd.append(ent.text)
  for index in range(len(label_list_jd)) : 
      if label_list_jd[index] in dic_jd.keys() : 
          dic_jd[label_list_jd[index]].append(text_list_jd[index])
      else : 
          dic_jd[label_list_jd[index]] = [text_list_jd[index]]
  dic_jd['program_details'] = list(final_program)
  dic_jd['Year_experience'] = extract_years_of_experience(jd_data_text)
  
  return dic_jd
