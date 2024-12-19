from decimal import Decimal
from typing import List
from pydantic import BaseModel # type: ignore
# Modèle pour la requête utilisateur
class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"

class RequestChain(BaseModel):
    host:str
    user:str
    password:str
    database:str
    query:str
    model:str ="gpt-3.5-turbo"
    
class TestRequest(BaseModel):
    message:str

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

class EmailRequest(BaseModel):
    email: str
    candidates: List[Candidate]

class JobRequest(BaseModel):
    host:str
    user:str
    password:str
    database:str
    query: str="select IDjob from applications;"