from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.client import HTTPException
from smtplib import SMTP
import smtplib
from typing import List
from requestData import Candidate
from database import getData
from sqlalchemy import create_engine # type: ignore

EMAIL_CONFIG = {
    "smtp_server": "smtp.mail.yahoo.com",
    "smtp_port": 587,
    "username": "yiyuemej@yahoo.fr",
    "password": "vkpknbjvbyjphgbj",
}

def send_email_with_gmail(recipient_email: str, candidates: List[Candidate]):
    try:
        # Création du contenu de l'email
        subject = "Top Candidates for the Selected Role"
        body = """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
        Bonjour, <br/>
        
            <h1>Top  Candidates </h1>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Experience</th>
                        <th>Certifications</th>
                        <th>Diplome</th>
                        <th>Soft Skills</th>
                        <th>Hard Skills</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Ajout des lignes des candidats au tableau
        for candidate in candidates:
            body += f"""
                    <tr>
                        <td>{candidate.applicantName}</td>
                        <td>{candidate.Score}</td>
                        <td>{candidate.Experience}</td>
                        <td>{candidate.Certification}</td>
                        <td>{candidate.Diplome}</td>
                        <td>{candidate.Soft}</td>
                        <td>{candidate.Hard}</td>
                    </tr>
            """

        body += """
                </tbody>
            </table>
        </body>
        </html>
        """

        # Configuration du message
        msg = MIMEMultipart()
        msg['From'] = "yiyuemej@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('yiyuemej@yahoo.fr', 'vkpknbjvbyjphgbj')
        server.sendmail('yiyuemej@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
        
        


        

  