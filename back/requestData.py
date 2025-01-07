from datetime import date
from decimal import Decimal
from typing import List
from pydantic import BaseModel # type: ignore
# Modèle pour la requête utilisateur

class Candidate(BaseModel):
    applicantName: str
    Score:float
    Experience: int
    Diplome: str
    Soft: str
    Hard: str
    Certification:str
   
class CandidateRequest(BaseModel):
    role_id: str
    top_n: int
class CandidateRequest3(BaseModel):
    role_id: str
    start_date: date 
    end_date:date

class CandidateRequest2(BaseModel):
    role_id: str
    
    
class EmailRequest(BaseModel):
    email: str
    candidates: List[Candidate]

class JobRequest(BaseModel):
    host:str
    user:str
    password:str
    database:str
    query: str="select IDjob from applications;"

class ExperienceData(BaseModel):
    Experience: int
    NombreDeCandidats: int

class JobData(BaseModel):
    IDjob:str
    Role:str
    date:date
    experience:int
    diplome:str
    certification:str
    hard:str
    soft:str

class ApplicationData(BaseModel):
    IDapp:str
    IDjob:str
    Role:str
    Date:date
    Score:float
    applicantName: str
    Experience: int
    Diplome: str
    Soft: str
    Hard: str
    Certification:str
class EmailRequest2(BaseModel):
    email: str
    applications: List[ApplicationData]

class EmailRequest3(BaseModel):
    email: str
    applications: List[ApplicationData]
    topN:int

class Candidate2(BaseModel):
    applicantName: str
    Score:float
    Experience: int
    Date:date