from datetime import datetime
from typing import List
from database import get_db_connection
from requestData import Candidate, CandidateRequest, ChatRequest, EmailRequest, JobRequest, RequestChain, TestRequest
from utils import chat_gpt, getData, langchain_agent, langchain_agent_sql, send_email_with_gmail
from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.responses import FileResponse # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import openai # type: ignore
import os
from dotenv import load_dotenv # type: ignore
XML_FOLDER = "../front/demo-ask/public/data"
os.makedirs(XML_FOLDER, exist_ok=True)

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origine autorisée (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes
)


@app.get("/")
def root():
    return {"message": "Welcome to ASK API @copyright by Bright-Technology"}



@app.post("/candidates", response_model=List[Candidate])
def get_top_candidates(request: CandidateRequest):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = (
                "SELECT applicantName, Score,Experience, Certification, Diplome, Soft, Hard "
                "FROM applications WHERE IDjob = %s ORDER BY Score DESC LIMIT %s"
            )
            cursor.execute(query, (request.role_id, request.top_n))
            candidates = cursor.fetchall()
            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found for the specified role.")
            return candidates
    finally:
        connection.close()
@app.post("/send-email")
def send_email(request: EmailRequest):
    send_email_with_gmail(request.email, request.candidates)
    return {"message": f"Email successfully sent to {request.email}"}

@app.get("/role")
async def getRole():
     response=getData(host="192.168.1.181",user="jordan",db="aubay",password="jordan",query="select IDjob from applications;")

     return {"message":response}