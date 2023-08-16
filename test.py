from deep_translator import GoogleTranslator
from langdetect import detect
from src.data_ingestion.file_reader import read_file
from src.data_preprocessing.resume_preprocessing import resume_preprocessing_model
from gensim.models.doc2vec import Doc2Vec

import pandas as pd
path = 'data/raw_data'
def detect_lang(resume_text) :
  lang = detect(resume_text)
  if lang == 'fr' :
    print('yes it is french')
    final_text=list()
    for i in range(0, len(resume_text), 50000):
      print('i am in the iteration num' + str(i))
      translation = GoogleTranslator(source='auto', target='en').translate(resume_text[i:i+50000], dest='en')
      final_text.append(translation)
    return ' '.join(final_text) 
  else : 
    return resume_text
resume_example = read_file('CV_Ahmed_Farhat.pdf',path)
#preprocessed_resume = preprocess_resume_text(resume_example)
preprocessed_resume = resume_preprocessing_model(resume_example['content'])

scores = pd.read_csv('data/scores.csv') 
model_80 = Doc2Vec.load('resumes_model_epochs_80.model')
model_100 = Doc2Vec.load('resumes_model_epochs_80.model')
model_150 = Doc2Vec.load('resumes_model_epochs_80.model')
models = [{'name': 'model80','model':model_80},
          {'name': 'model100','model':model_100},
          {'name': 'model150','model':model_150},
    ]
res = dict()
res=extract_all_info(elem['content'],skill_extractor)
for jd in jds : 
    jd_info = get_jd_info(jd['value'],skill_extractor)
    for model in models : 
        overall = overall_similarity(jd['value'],elem['content'],model['model'])
        info = match_profile(jd_info,res,weights) 
        final_result = similarity_aggreg(overall,info,model_weights)
        results.append({'model':model['name'],'type':jd['name'],'name':elem['name'],'similarity':final_result})
