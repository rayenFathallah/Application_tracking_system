import  pymongo 
def get_connect() : 
    client = pymongo.MongoClient("localhost",27017)
    return client