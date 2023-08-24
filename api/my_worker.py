'''
import os
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
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
skills_model = spacy.load('models/model-best')

'''
import celery
celery_app = celery.Celery('my_worker',broker='amqp://guest:guest@localhost:15672')
from initializer import resume
from celery import shared_task
#os.environ['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379'
#os.environ['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379'
#@shared_task(name="my_task",ignore_result=True) 
def my_task(element) : 
    resume_obj = resume(element)
    resume_obj.insert_resume()