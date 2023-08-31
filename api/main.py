from initializer import resume
import tika
import pandas as pd
import os
from src.data_ingestion.file_reader import read_files
from connector import get_connect 

file_names = os.listdir('./data/raw_data')
path = 'data/raw_data'

tika.initVM()
resumes_list = read_files(file_names,path)
for elem in resumes_list : 
    resume_elem = resume(elem) 
    resume_elem.insert_resume()

