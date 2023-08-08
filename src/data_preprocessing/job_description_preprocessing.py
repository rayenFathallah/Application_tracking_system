import pandas as pd 
import sys
from src.exception import CustomException
from src.logger import logging
from src.data_preprocessing.resume_preprocessing import extract_skills
def get_skills_jd(job_description) : 
    jd_skills = []
    try : 
        jd_skills = extract_skills(job_description) 
        return jd_skills 
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while Extracting the skillls from descriptions: " + str(e))
        return jd_skills
def get_all_skills_jd(jobs) : 
    all_skills = []
    try : 
        for job in jobs : 
            res = get_skills_jd(job)
            all_skills.append(res) 
        return all_skills
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while Extracting the skillls from descriptions: " + str(e))
        return all_skills