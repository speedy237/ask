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
    "smtp_server": "smtp.gmail.com ",
    "smtp_port": 587,
    "username": "gael.kamdemdeteyou@gmail.com",
    "password": "dhzd ycws kerq dhcb",
}

def create_custom_xml_from_any_data(data, output_file):
    """
    Convertit n'importe quel tableau de dictionnaires en format XML avec des balises <label> et <value>.
    
    :param data: Liste de dictionnaires avec des paires clé-valeur
    :param output_file: Chemin du fichier XML à créer
    """
    # Créer la racine XML
    root = ET.Element("data")

    for record in data:
        entry = ET.SubElement(root, "entry")

        for key, value in record.items():
            label = ET.SubElement(entry, "label")
            label.text = str(key)

            val = ET.SubElement(entry, "value")
            val.text = str(value)

    # Convertir l'arbre XML en chaîne et l'écrire dans un fichier
    tree = ET.ElementTree(root)
    with open(output_file, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

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
        msg['From'] = "gael.kamdemdeteyou@gmail.com"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.gmail.com ', 587)
        server.starttls()
        server.login('gael.kamdemdeteyou@gmail.com', 'dhzd ycws kerq dhcb')
        server.sendmail('gael.kamdemdeteyou@gmail.com', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
        
        


        

  