from fastapi import APIRouter, Path, Query, Request, HTTPException,Response
from bson.json_util import dumps
from bson import ObjectId
from api.connector import get_connect 
router = APIRouter ()
conn = get_connect()
@router.get("/get_jobs")
async def get_all_jobs():
    db=conn.ATS_db 
    jobs_db = db["jobs"]
    query = {"open":True}
    jobs = jobs_db.find(query)
    list_cur = list(jobs)
    return dumps(list_cur) 

@router.get('/get_job') 
async def get_job(job_title):
    db=conn.ATS_db 
    jobs_db = db["jobs"]
    query = {"open":True,"title":job_title}
    jobs = jobs_db.find(query)
    list_cur = list(jobs)
    if len(list_cur)> 1 : 
        raise HTTPException(status_code=404, detail="More than one job found")
    return dumps(list_cur) 

@router.put('/update_job') 
async def update_job(job_id:str,new_job:dict):
    db=conn.ATS_db 
    jobs_db = db["jobs"]
    id = ObjectId(job_id)
    query = {"_id":id}
    update = {"$set": {"title": new_job["title"], "text": new_job["text"]}}
    result = jobs_db.update_one(query, update)
    if result.modified_count == 1:
         return Response(content="Job updated successfully", status_code=200)
    else:
        return Response(content="Job not found", status_code=404)


@router.get('/get_resumes') 
async def get_all_resumes():
    db=conn.ATS_db 
    resumes_db = db["resumes"]
    query = {"open":True}
    resumes = resumes_db.find(query)
    list_cur = list(resumes)
    return dumps(list_cur) 

@router.get('/get_job_resumes') 
async def get_job_resumes(job_id):
    db=conn.ATS_db 
    resumes_db = db["resumes"]
    id = ObjectId(job_id)
    query = {"_id":id,"open":True}
    resumes = resumes_db.find(query)
    list_cur = list(resumes)
    return dumps(list_cur) 

@router.get('/get_similarities')
async def get_similarities(resumes,job_text) : 
    '''
    just do smth here
    '''
