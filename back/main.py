from datetime import datetime
from typing import List
from database import get_db_connection
from requestData import ApplicationData, Candidate, Candidate2, CandidateRequest, CandidateRequest2, CandidateRequest3, EmailRequest, EmailRequest2, EmailRequest3, ExperienceData, JobData
from utils import create_custom_xml_from_any_data, getData, send_email, send_email2, send_email3, send_email_with_gmail
from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.responses import FileResponse # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import os

XML_FOLDER = "../front/demo-ask/public/data"
os.makedirs(XML_FOLDER, exist_ok=True)


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



@app.post("/top_candidate", response_model=List[Candidate])
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
def send_email_candidate(request: EmailRequest3):
    send_email2(request.email, request.applications,request.topN)
    return {"message": f"Email successfully sent to {request.email}"}

@app.get("/role")
async def getRole():
     response=getData(host="localhost",user="root",db="aubay",password="",query="select IDjob, Role from job;")

     return {"message":response}

@app.post("/getXMLFile/")
def get_xml_file(data: list[dict]): # type: ignore
    """
    Génère un fichier XML à partir des données et le retourne.
    :param data: Liste de tuples [(label, value), ...]
    """
    if not data:
        raise HTTPException(status_code=400, detail="Data is required to generate XML.")
    
    # Génération du nom de fichier avec la date
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"input_data_{current_date}.xml"
    output_file = os.path.join(XML_FOLDER, filename)
    
    create_custom_xml_from_any_data(data, output_file)
    
    return {"filename":filename}

@app.get("/all", response_model=List[ApplicationData])
def get_all_candidates():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query ="SELECT * FROM applications ORDER BY IDjob, Score DESC;"
            cursor.execute(query)
            candidates = cursor.fetchall()
            if not candidates:
                raise HTTPException(status_code=404, detail="Not Found candidates")
            return candidates
    finally:
        connection.close()


@app.get("/role/all", response_model=List[JobData])
def get_all_candidates():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query ="SELECT * from job;"
            cursor.execute(query)
            jobs = cursor.fetchall()
            if not jobs:
                raise HTTPException(status_code=404, detail="Not Found candidates")
            return jobs
    finally:
        connection.close()


@app.post("/experience/", response_model=List[ExperienceData])
def get_all_experience(request: CandidateRequest2):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = (
                "SELECT Experience, COUNT(*) AS NombreDeCandidats "
                "FROM applications WHERE IDjob = %s GROUP BY Experience ORDER BY 2 DESC;"
            )
            cursor.execute(query, (request.role_id,))
            candidates = cursor.fetchall()
            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found for the specified role.")
            return [{"Experience": row["Experience"], "NombreDeCandidats": row["NombreDeCandidats"]} for row in candidates]
    finally:
        connection.close()

@app.post("/role/candidate", response_model=List[Candidate2])
def get_Newcandidates(request: CandidateRequest3):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = (
                "SELECT applicantName, Score, Experience, Date "
                "FROM applications "
                "WHERE IDjob = %s AND Date BETWEEN %s AND %s "
                "ORDER BY Score DESC"
            )
            cursor.execute(query, (request.role_id, request.start_date, request.end_date))
            candidates = cursor.fetchall()
            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found for the specified role and date range.")
            return candidates
    finally:
        connection.close()


@app.post("/role/candidate/old", response_model=List[Candidate2])
def get_Oldcandidates(request: CandidateRequest2):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = (
                "SELECT applicantName, Score, Experience,Date "
                "FROM applications "
                "WHERE IDjob = %s"
                "ORDER BY Score DESC"
            )
            cursor.execute(query, (request.role_id))
            candidates = cursor.fetchall()
            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found for the specified role and date range.")
            return candidates
    finally:
        connection.close()