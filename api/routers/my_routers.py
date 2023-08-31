from fastapi import APIRouter,HTTPException,Response
from bson.json_util import dumps
import json
import time
from bson import ObjectId
from api.connector import get_connect 
from api.src.data_preprocessing.job_description_preprocessing import get_jd_info
from api.src.similarity import get_final_similarity
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

router = APIRouter ()
conn = get_connect()
weights = {'skills':100,'niveau':0,'experience':0}
model_weights = {'overall' : 0.4,'info':0.4,'tf_idf':0.2}

class JobCreate(BaseModel):
    title: str
    description: str

async def process_job(job: JobCreate):
    # Load the skills_model (this might take some time)
    try : 
        infos = get_jd_info(job.description)
        infos['title'] = job.title
        infos['text'] = job.description
    except : 
        return "probleme men haja okra"
    return infos
@router.post('/post_job')
async def post_job(my_job: JobCreate):

    try:
        db = conn.ATS_db
        jobs_db = db["jobs"]
        try:
            task = process_job(my_job)
        except:
            print("Exception raised in process_job()")
            return "problem processing"

        # Wait for the task to complete
        result = await task
        # Get the result of the insert operation
        result['open']=True
        insert_result = jobs_db.insert_one(result)

        # Check if the insert operation was successful
        if insert_result.acknowledged:
            return "Sucess"
        else:
            return "problem accured while executing the query";

    except Exception as e:
        # Handle exceptions gracefully, perhaps log the error
        print("Exception raised: {}".format(e))
        return "problem accured {}".format(e)


@router.get("/get_jobs")
async def get_all_jobs():
    db=conn.ATS_db 
    jobs_db = db["jobs"]
    query = {"open":True}
    jobs = jobs_db.find()
    list_cur = list(jobs)
    results = []
    for elem in list_cur : 
        dumped = dumps(elem)
        json_form = json.loads(dumped)
        json_form["str_id"] = str(ObjectId(elem["_id"])) 
        results.append(json_form)
    return dumps(results) 

@router.get('/get_job/{job_title}') 
async def get_job(job_title):
    db=conn.ATS_db 
    jobs_db = db["jobs"]
    query = {"open":True,"title":job_title}
    jobs = jobs_db.find(query)
    list_cur = list(jobs)
    if len(list_cur)> 1 : 
        raise HTTPException(status_code=404, detail="More than one job found")
    element = list_cur[0]
    #element['str_id'] =str(ObjectId(list_cur[0]["_id"])) 
    dumped = dumps(element)
    json_form = json.loads(dumped)
    json_form["str_id"] = str(ObjectId(element["_id"])) 
    return dumps(json_form)

@router.put('/update_job/{job_id}') 
async def update_job(job_id:str,new_job:dict):
    db=conn.ATS_db 
    jobs_db = db["jobs"]
    id = ObjectId(job_id)
    query = {"_id":id}
    update = {"$set": {"title": new_job["title"], "text": new_job["text"],"SKILLS":new_job['SKILLS']}}
    result = jobs_db.update_one(query, update)
    if result.modified_count == 1:
         return Response(content="Job updated successfully", status_code=200)
    else:
        return Response(content="Job not found", status_code=404)

class Resume_get(BaseModel) : 
    str_id : str

@router.get("/get_institutes")  
async def get_inst() : 
    db=conn.ATS_db 
    distinct_institutes = []
    inst_db = db["institutes"]
    res = inst_db.distinct("name")
    return res
@router.get("/get_niveaux")  
async def get_niveaux() : 
    db=conn.ATS_db 
    distinct_niveaux = []
    resumes_db = db["resumes"]
    for document in resumes_db.find():
        for niveau in document["infos"]["education"]["niveau_exacte"]:
            if niveau not in distinct_niveaux:
                distinct_niveaux.append(niveau)
    return distinct_niveaux
@router.get("/resume/{resume_id}") 
async def get_resume(resume_id : str):
    db=conn.ATS_db 
    resumes_db = db["resumes"]
    id = ObjectId(resume_id)
    query = {"open":True,"_id":id}
    resumes = resumes_db.find(query)
    list_cur = list(resumes)
    if len(list_cur)> 1 : 
        raise HTTPException(status_code=404, detail="More than one resume found")
    element = list_cur[0]
    #element['str_id'] =str(ObjectId(list_cur[0]["_id"])) 
    dumped = dumps(element)
    json_form = json.loads(dumped)
    json_form["str_id"] = str(ObjectId(element["_id"])) 
    return dumps(json_form)

@router.put('/get_all_resumes') 
async def get_job_resumes(job_id : Resume_get):
    job = {}
    try : 
        db=conn.ATS_db 
        resumes_db = db["resumes"]
        if(job_id.str_id!="") :
            job = db["jobs"].find_one({"_id": ObjectId(job_id.str_id)})
    except : 
        return "problem connection to db"
    try : 
        resumes = resumes_db.find() 
        list_cur = list(resumes)  
        results = []
        start_time = time.time()  # Record the start time

        for elem in list_cur : 
            dumped = dumps(elem)
            #score = get_final_similarity(json_form,job)
            json_form = json.loads(dumped)
            json_form["str_id"] = str(ObjectId(elem["_id"])) 
            if(job_id.str_id!="") :
                score=get_final_similarity(job,elem)
                json_form['score'] = int(score)
            results.append(json_form)
        end_time = time.time()  # Record the start time
        elapsed_time = end_time - start_time

        return dumps(results)
    except : 
        return "problem accured"
## Parallel version _____________________________________________________________ 


@router.put('/get_all_resumes2')
async def get_job_resumes(job_id: Resume_get):
    try:
        db = conn.ATS_db
        resumes_db = db["resumes"]
        if job_id.str_id != "":
            job = db["jobs"].find_one({"_id": ObjectId(job_id.str_id)})
    except:
        return "problem connection to db"

    try:
        resumes = resumes_db.find()
        list_cur = list(resumes)
        results = []

        def process_elem(elem):
            dumped = dumps(elem)
            json_form = json.loads(dumped)
            json_form["str_id"] = str(ObjectId(elem["_id"]))
            if job_id.str_id != "":
                
                score = get_final_similarity(job, elem)
                json_form['score'] = int(score)
            results.append(json_form)
        start_time = time.time()  # Record the start time
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(process_elem, list_cur)
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        return dumps(results)
    except:
        return "problem occurred"
# ____________________________________________________________________

@router.put ('/get_job_resumes') 
async def get_job_resumes(job_id : Resume_get):
    try : 
        db=conn.ATS_db 
        resumes_db = db["resumes"]
        #query = {"job_id":job_id.str_id}
        query = {
        "job_id": {
            "$in": [job_id.str_id]
        }
        }
        job = db["jobs"].find_one({"_id": ObjectId(job_id.str_id)})
    except : 
        return "problem connection to db"
    try : 
        resumes = resumes_db.find(query) 
        list_cur = list(resumes)  
        results = []
        for elem in list_cur : 
            dumped = dumps(elem)
            #score = get_final_similarity(json_form,job)
            json_form = json.loads(dumped)
            json_form["str_id"] = str(ObjectId(elem["_id"])) 
            job_index = json_form["job_id"].index(job_id.str_id)
            #score=get_final_similarity(job,elem)
            json_form['score'] = int(json_form["job_scores"][job_index])
            results.append(json_form)
        return dumps(results)
    except : 
        return "Unknown problem accured"
class Resume_update(BaseModel) : 
    new_status : str
    resume_id : str
    job_id : str


@router.put('/update_candidate_status') 
async def update_candidate_status(update : Resume_update):
    try : 
        db=conn.ATS_db 
        resumes_db = db["resumes"]
        id = ObjectId(update.resume_id)
        query = {"_id":id}
        try :
            job = db["jobs"].find_one({"_id": ObjectId(update.job_id)})
        except : 
            return "probleme mel database "
        update_query = {"$set": {"status":update.new_status}}
        resume = resumes_db.find_one(query)
        job_index = resume["job_id"]
        scores_index = resume["job_scores"]
        if(update.job_id in job_index) :
            result = resumes_db.update_one(query, update_query)
        else:
            score=get_final_similarity(job,resume)
            job_index.append(update.job_id)
            scores_index.append(score)

  # The job id is not present, so update the status and add the job
            update2 = {
                "$set": {
                "status":update.new_status,
                "job_id": job_index,
                "job_scores" : scores_index
                }
            }
            result = resumes_db.update_one(query, update2)

        return Response(content="candidate status updated successfully", status_code=200)

    except : 
        return Response(content="Candidate not found", status_code=404) 
    '''
    if result.modified_count == 1:
         return Response(content="candidate status updated successfully", status_code=200)
    else:
        return Response(content="Candidate not found", status_code=404) 
        '''
