
from worker.my_worker import my_task
from fastapi import FastAPI
from src.data_ingestion.file_reader import read_files
import os
import tika
import celery
import asyncio
fast_app = FastAPI()
file_names = os.listdir('./data/test_data')
path = 'data/test_data'
tika.initVM()
resumes_list = read_files(file_names,path)
@fast_app.post("/trigger-task")
def trigger_task() : 
    for element in resumes_list:
        my_task.delay(element)
    return "tasks enqueued successfully"
# Wait for all tasks to complete


