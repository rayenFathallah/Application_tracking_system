import pandas as pd 
import spacy 
import tika 
import re
from src.data_preprocessing.resume_preprocessing import detect_lang,extract_years_of_experience,remove_accents
def get_jd_info(jd_data_text,jd_model) :
  dic_jd = {}
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
  dic_jd['after_bac'] = detect_niveau(matches_bac[0]) 
  
  return dic_jd
def detect_niveau(years_after_bac) : 
    matching_dic = { 
        '3' : ['licence'], 
        '5' : ['ingernieurie','mastere'],
        '6' : ['ingenieurie','mastere'],
        '9' : ['doctorat']
    }
    if str(years_after_bac) in matching_dic.keys() : 
        return matching_dic[str(years_after_bac)]
    else : 
        return []
    
