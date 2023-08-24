
from my_worker import my_task
from fastapi import FastAPI
from src.data_ingestion.file_reader import read_files
from fastapi.middleware.cors import CORSMiddleware  
import os
import tika
import celery
from routers import my_routers
fast_app = FastAPI()
fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
file_names = os.listdir('./data/test_data')
path = 'data/test_data'
tika.initVM()
#resumes_list = read_files(file_names,path)
#@fast_app.post("/trigger-task")
'''
def trigger_task() : 
    for element in resumes_list:
        my_task.delay(element)
    return "tasks enqueued successfully"
'''
# Wait for all tasks to complete
@fast_app.get("/") 
def home():
    return "Hello, World!"
fast_app.include_router(my_routers.router)
