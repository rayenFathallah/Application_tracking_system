from api.src.data_preprocessing.job_description_preprocessing import get_jd_info
from dataclasses import dataclass, asdict
import spacy
@dataclass
class job : 
    Title : str
    Text : str 
    currently_open : bool
    def __init__(self,Title,Text,currently_open=True) : 
        self.Title = Title 
        self.Text = Text 
        skills_model = spacy.load('api/models/model-best')
        self.currently_open = currently_open
        infos = get_jd_info(Text,skills_model) 
        self.infos = infos
    def get_job(self) : 
        return {"title":self.Title,"text" : self.Text,"infos":self.infos}
    
    