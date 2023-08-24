from initializer import resume
import tika
import os
from src.data_ingestion.file_reader import read_files
file_names = os.listdir('./data/test_data')
path = 'data/test_data'
tika.initVM()
resumes_list = read_files(file_names,path)
for elem in resumes_list : 
    resume_elem = resume(elem) 
    resume_elem.insert_resume()
