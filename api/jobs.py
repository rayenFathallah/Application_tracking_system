from pydantic import BaseModel
class job(BaseModel) : 
    Title : str
    Text : str 
    currently_open : bool
    