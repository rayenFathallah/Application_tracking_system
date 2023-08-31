import os
import sys

from src.data_preprocessing.resume_preprocessing import extract_all_info
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from spacy.matcher import PhraseMatcher
import spacy
from connector import get_connect
client = get_connect()
db=client.ATS_db 
resume_db = db["resumes"]
nlp = spacy.load("en_core_web_lg")
#skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
skills_model = spacy.load('models/model-best')
class resume : 
    def __init__(self,resume) : 
        self.text = resume['content']
        self.binary = resume['binary'] 
        self.name = resume['name']
    def get_info(self) : 
        #self.infos=extract_all_info(self.text,skill_extractor,skills_model) 
        self.infos=extract_all_info(self.text,skills_model) 

    def prepare_results(self) :
        self.get_info() 
        res = dict() 
        res['text'] = self.text 
        res['infos'] = self.infos 
        res['binary'] = self.binary 
        res['name'] = self.name
        res['status'] = 'waiting' 
        res['open']= True
        res['job_id'] = []
        res['job_scores']=[]
        return res 
    def insert_resume(self) : 
        result = self.prepare_results()
        resume_db.insert_one(result)
